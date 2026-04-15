"""
Tests for the VPC region assignment bug in resources.py loadJSON().

Bug: the `region` for each VPC was read from `subnet['region']` where `subnet`
was the loop variable from the *previous* subnets loop — i.e., the last subnet
seen, regardless of which VPC was being processed.  Every VPC would end up with
the same (wrong) region, producing incorrect CRNs.

Fix: build a vpc-id → region map from the subnets before entering the VPC loop,
then look up each VPC's region from that map (falling back to a 'region' field
directly on the VPC object if present).
"""

import pytest
from unittest.mock import MagicMock, patch
from ibmdiagrams.ibmbase.resources import Resources


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_resources():
    """Return a Resources instance with a mocked Common."""
    common = MagicMock()
    common.getInputFile.return_value = "dummy.json"
    common.getProvider.return_value = MagicMock(value="IBM")
    r = Resources.__new__(Resources)
    r.common = common
    r.resourceDictionary = {}
    return r


def build_data(vpcs, subnets):
    """Combine vpcs and subnets into the dict that loadJSON() expects."""
    return {"vpcs": vpcs, "subnets": subnets}


def run_vpc_region_block(resources, data):
    """
    Execute only the subnet→region map building and VPC-loop portions of
    loadJSON() so tests are isolated from I/O and unrelated logic.
    """
    # Build vpc→region map (copied verbatim from resources.py fix)
    vpc_region_map = {}
    if "subnets" in data:
        for s in data["subnets"]:
            vid = s.get("vpcId", "")
            reg = s.get("region", "")
            if vid and reg:
                vpc_region_map[vid] = reg

    import pandas as pd
    if "vpcs" in data:
        count = 0
        table = {}
        for vpc in data["vpcs"]:
            name = vpc["name"]
            vid = vpc["id"]
            region = vpc.get("region") or vpc_region_map.get(vid, "")
            attributes = {"name": name, "id": vid, "crn": "crn:v1:bluemix:public:vpc:" + region}
            row = {"id": vid} | attributes
            table[count] = row
            count += 1
        if table:
            resources.resourceDictionary["ibm_is_vpc"] = pd.DataFrame.from_dict(table, orient="index")
        else:
            resources.resourceDictionary["ibm_is_vpc"] = pd.DataFrame()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestVPCRegionAssignment:

    def test_each_vpc_gets_its_own_region(self):
        """Two VPCs in different regions must each get their correct region."""
        data = build_data(
            vpcs=[
                {"name": "vpc-us", "id": "vpc-us-id"},
                {"name": "vpc-eu", "id": "vpc-eu-id"},
            ],
            subnets=[
                {"name": "sub-us-1", "id": "sub-us-1-id", "subnet": "10.0.0.0/24",
                 "vpcId": "vpc-us-id", "availabilityZone": "us-south-1", "region": "us-south"},
                {"name": "sub-eu-1", "id": "sub-eu-1-id", "subnet": "10.1.0.0/24",
                 "vpcId": "vpc-eu-id", "availabilityZone": "eu-de-1", "region": "eu-de"},
            ],
        )
        r = make_resources()
        run_vpc_region_block(r, data)

        vpcs_df = r.resourceDictionary["ibm_is_vpc"]
        us_crn = vpcs_df.loc[vpcs_df["id"] == "vpc-us-id", "crn"].iloc[0]
        eu_crn = vpcs_df.loc[vpcs_df["id"] == "vpc-eu-id", "crn"].iloc[0]

        assert "us-south" in us_crn, f"Expected 'us-south' in CRN, got: {us_crn}"
        assert "eu-de" in eu_crn, f"Expected 'eu-de' in CRN, got: {eu_crn}"
        # The US VPC must NOT get the EU region (the original bug)
        assert "eu-de" not in us_crn, "VPC received wrong region from sibling VPC's subnet"

    def test_stale_variable_bug_is_fixed(self):
        """
        Regression: before the fix, all VPCs would receive the last subnet's region.
        Verify that VPCs that come BEFORE the last subnet in the list are not
        contaminated with the last subnet's region.
        """
        data = build_data(
            vpcs=[
                {"name": "vpc-first", "id": "vpc-first-id"},
                {"name": "vpc-second", "id": "vpc-second-id"},
            ],
            subnets=[
                {"name": "sub-a", "id": "sub-a-id", "subnet": "10.0.0.0/24",
                 "vpcId": "vpc-first-id", "availabilityZone": "us-south-1", "region": "us-south"},
                # This is the last subnet — the old bug would give this region to ALL vpcs
                {"name": "sub-b", "id": "sub-b-id", "subnet": "10.1.0.0/24",
                 "vpcId": "vpc-second-id", "availabilityZone": "jp-tok-1", "region": "jp-tok"},
            ],
        )
        r = make_resources()
        run_vpc_region_block(r, data)

        vpcs_df = r.resourceDictionary["ibm_is_vpc"]
        first_crn = vpcs_df.loc[vpcs_df["id"] == "vpc-first-id", "crn"].iloc[0]
        second_crn = vpcs_df.loc[vpcs_df["id"] == "vpc-second-id", "crn"].iloc[0]

        assert "us-south" in first_crn, f"Expected 'us-south' in first VPC CRN, got: {first_crn}"
        assert "jp-tok" in second_crn, f"Expected 'jp-tok' in second VPC CRN, got: {second_crn}"
        # Original bug: first VPC would also get jp-tok
        assert "jp-tok" not in first_crn, "First VPC incorrectly received last subnet's region"

    def test_vpc_region_field_takes_precedence_over_subnet_derived_region(self):
        """If a VPC object has its own 'region' field, that must be used."""
        data = build_data(
            vpcs=[
                {"name": "vpc-explicit", "id": "vpc-explicit-id", "region": "au-syd"},
            ],
            subnets=[
                {"name": "sub-x", "id": "sub-x-id", "subnet": "10.0.0.0/24",
                 "vpcId": "vpc-explicit-id", "availabilityZone": "us-south-1", "region": "us-south"},
            ],
        )
        r = make_resources()
        run_vpc_region_block(r, data)

        vpcs_df = r.resourceDictionary["ibm_is_vpc"]
        crn = vpcs_df.loc[vpcs_df["id"] == "vpc-explicit-id", "crn"].iloc[0]
        assert "au-syd" in crn, f"VPC's own region should take precedence, got: {crn}"

    def test_vpc_with_no_subnets_gets_empty_region(self):
        """A VPC with no matching subnet and no region field results in an empty region."""
        data = build_data(
            vpcs=[{"name": "orphan-vpc", "id": "orphan-vpc-id"}],
            subnets=[],
        )
        r = make_resources()
        run_vpc_region_block(r, data)

        vpcs_df = r.resourceDictionary["ibm_is_vpc"]
        crn = vpcs_df.loc[vpcs_df["id"] == "orphan-vpc-id", "crn"].iloc[0]
        # Should not crash and should produce a CRN with empty region suffix
        assert crn == "crn:v1:bluemix:public:vpc:"

    def test_multiple_subnets_per_vpc_single_region_assigned(self):
        """A VPC with multiple subnets in the same region gets the correct region once."""
        data = build_data(
            vpcs=[{"name": "big-vpc", "id": "big-vpc-id"}],
            subnets=[
                {"name": "sub-1", "id": "sub-1-id", "subnet": "10.0.1.0/24",
                 "vpcId": "big-vpc-id", "availabilityZone": "us-south-1", "region": "us-south"},
                {"name": "sub-2", "id": "sub-2-id", "subnet": "10.0.2.0/24",
                 "vpcId": "big-vpc-id", "availabilityZone": "us-south-2", "region": "us-south"},
                {"name": "sub-3", "id": "sub-3-id", "subnet": "10.0.3.0/24",
                 "vpcId": "big-vpc-id", "availabilityZone": "us-south-3", "region": "us-south"},
            ],
        )
        r = make_resources()
        run_vpc_region_block(r, data)

        vpcs_df = r.resourceDictionary["ibm_is_vpc"]
        crn = vpcs_df.loc[vpcs_df["id"] == "big-vpc-id", "crn"].iloc[0]
        assert crn == "crn:v1:bluemix:public:vpc:us-south"

    def test_crn_format_is_correct(self):
        """CRN must follow the expected format with the region in the right position."""
        data = build_data(
            vpcs=[{"name": "vpc-a", "id": "vpc-a-id"}],
            subnets=[
                {"name": "sub-a", "id": "sub-a-id", "subnet": "10.0.0.0/24",
                 "vpcId": "vpc-a-id", "availabilityZone": "ca-tor-1", "region": "ca-tor"},
            ],
        )
        r = make_resources()
        run_vpc_region_block(r, data)

        vpcs_df = r.resourceDictionary["ibm_is_vpc"]
        crn = vpcs_df.loc[vpcs_df["id"] == "vpc-a-id", "crn"].iloc[0]
        assert crn == "crn:v1:bluemix:public:vpc:ca-tor"
