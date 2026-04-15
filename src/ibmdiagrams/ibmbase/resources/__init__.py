# @file __init__.py
#
# Copyright contributors to the ibmdiagrams project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""IBM Cloud resource definitions organized by category."""

import os.path
import pandas as pd
from json import loads as json_load, dumps as json_dumps
from tabulate import tabulate
from ipaddress import ip_network, ip_address

from .compute import COMPUTE_RESOURCES
from .network import NETWORK_RESOURCES
from .storage import STORAGE_RESOURCES
from .database import DATABASE_RESOURCES
from .security import SECURITY_RESOURCES
from .containers import CONTAINER_RESOURCES
from .observability import OBSERVABILITY_RESOURCES

# Aggregate all resource dictionaries into a single dictionary
RESOURCE_DICTIONARY = {
    **COMPUTE_RESOURCES,
    **NETWORK_RESOURCES,
    **STORAGE_RESOURCES,
    **DATABASE_RESOURCES,
    **SECURITY_RESOURCES,
    **CONTAINER_RESOURCES,
    **OBSERVABILITY_RESOURCES,
}


class Resources:
    """Manages IBM Cloud resource definitions and Terraform state loading."""
    resourceDictionary = RESOURCE_DICTIONARY

    common = None

    def __init__(self, common):
        self.common = common

    def getResourceDictionary(self):
        return self.resourceDictionary

    def getResource(self, name):
        if name in self.resourceDictionary:
            resource = self.resourceDictionary[name]
        else:
            resource = pd.DataFrame()
        return resource

    def loadResources(self):
        if not os.path.isfile(self.common.getInputFile()):
            return False

        try:
            with open(self.common.getInputFile(), 'r', encoding='utf-8-sig') as stream:
                data = json_load(stream.read())
        except OSError:
            self.common.printInvalidFile(self.common.getInputFile())
            return False
        except ValueError:
            # json.JSONDecodeError is a subclass of ValueError
            self.common.printInvalidFile(self.common.getInputFile())
            return False
        resourcedata = data['resources']
        df = pd.json_normalize(resourcedata)

        for resource in self.resourceDictionary:
            count = 0
            table = {}

            for instances in df[df["type"] == resource]["instances"]:
                for instance in instances:
                    attributes = instance["attributes"]
                    id = attributes["id"]
                    row = {"id": id} | attributes
                    # print()
                    # print(resource)
                    # print(row)
                    # print()
                    table[count] = row
                    count += 1

            if table != {}:
                frame = pd.DataFrame.from_dict(table, orient="index")
            else:
                frame = pd.DataFrame()

            self.resourceDictionary[resource] = frame

        self.combineResources()
        self.splitResources()

        return True

    def combineResources(self):
        self.combineEndpointGatewayIP()
        return

    # Combine needed fields in endpoint gateway IP with fields in endpoint gateway.
    # Note that (number of resources in ipresource) > (number of resources in mainresource),
    # therefore (number of resources in mainresource) is increased to (number of resources in ipresource).
    def combineEndpointGatewayIP(self):
        mainresource = self.resourceDictionary["ibm_is_virtual_endpoint_gateway"]
        ipresource = self.resourceDictionary["ibm_is_virtual_endpoint_gateway_ip"]
        subnetresource = self.resourceDictionary["ibm_is_subnet"]

        if mainresource.empty or ipresource.empty or subnetresource.empty:
            return

        maintable = mainresource.to_dict('index')
        newtable = {}
        count = 0

        for ipindex, iprow in ipresource.iterrows():
            for mainkey, mainvalue in maintable.items():
                mainid = mainvalue["id"]
                if mainid == iprow["gateway"]:
                    for subnetindex, subnetrow in subnetresource.iterrows():
                        ipaddress = iprow["address"]
                        subnetcidr = subnetrow["ipv4_cidr_block"]
                        subnetid = subnetrow["id"]
                        if ip_address(ipaddress) in ip_network(subnetcidr):
                            mainvalue["subnet"] = subnetid
                            mainvalue["address"] = ipaddress
                            if newtable == {}:
                                newtable = {count:  mainvalue.copy()}
                            else:
                                newtable.update({count:  mainvalue.copy()})
                            count = count + 1
                            break

        frame = pd.DataFrame.from_dict(newtable, orient="index")
        self.resourceDictionary["ibm_is_virtual_endpoint_gateway"] = frame

        return

    def splitResources(self):
        self.splitContainerSubnets()
        return

    # Split subnets in container for display of separate OpenShift icons.
    def splitContainerSubnets(self):
        mainresource = self.resourceDictionary["ibm_container_vpc_cluster"]
        # subnetresource = self.resourceDictionary["ibm_is_subnet"]

        # if mainresource.empty or subnetresource.empty:
        if mainresource.empty:
            return

        maintable = mainresource.to_dict('index')
        newtable = {}
        count = 0

        for mainkey, mainvalue in maintable.items():
            mainid = mainvalue["id"]
            mainname = mainvalue["name"]
            mainvpc = mainvalue["vpc_id"]
            mainzones = mainvalue["zones"]
            for zone in mainzones:
                newvalue = {'id': mainid, 'name': mainname, 'vpc_id': mainvpc, 'zones': [
                    {'name': zone['name'], 'subnet_id': zone['subnet_id']}]}
                if newtable == {}:
                    newtable = {count:  newvalue}
                else:
                    newtable.update({count:  newvalue})
                count = count + 1

        frame = pd.DataFrame.from_dict(newtable, orient="index")
        self.resourceDictionary["ibm_container_vpc_cluster"] = frame

        return

    def loadJSON(self):
        if not os.path.isfile(self.common.getInputFile()):
            return False

        instances = pd.DataFrame()
        subnets = pd.DataFrame()
        vpcs = pd.DataFrame()

        try:
            with open(self.common.getInputFile(), 'r', encoding='utf-8-sig') as stream:
                data = json_load(stream.read())
        except OSError:
            self.common.printInvalidFile(self.common.getInputFile())
            return False
        except ValueError:
            # json.JSONDecodeError is a subclass of ValueError
            self.common.printInvalidFile(self.common.getInputFile())
            return False

        # Map instances to name, primary_network_interface primary_ip address, id, primary_network_interface subnet, vpc+zone, vpc
        if 'instances' in data:
            count = 0
            table = {}
            instances = data['instances']

            for instance in instances:
                name = instance['name']
                id = instance['id']
                vpc = instance['vpcId']
                zone = instance['availabilityZone']
                nics = instance['networkInterfaces']
                nic = nics[0]
                subnet = nic['networkId']
                ip = nic['ip']
                attributes = {'name': name, 'id': id, 'vpc': vpc, 'zone': zone, 'primary_network_interface': [
                    {'primary_ip': [{'address': ip}], 'subnet': subnet}]}
                row = {"id": id} | attributes
                table[count] = row
                count += 1

            if table != {}:
                frame = pd.DataFrame.from_dict(table, orient="index")
            else:
                frame = pd.DataFrame()

            self.resourceDictionary['ibm_is_instance'] = frame

        # Map subnets to name, ipv4_cidr_block, id, vpc, vpc+zone
        if 'subnets' in data:
            count = 0
            table = {}
            subnets = data['subnets']

            for subnet in subnets:
                name = subnet['name']
                id = subnet['id']
                cidr = subnet['subnet']
                vpc = subnet['vpcId']
                zone = subnet['availabilityZone']
                attributes = {'name': name, 'id': id, 'vpc': vpc,
                              'zone': zone, 'ipv4_cidr_block': cidr}
                row = {"id": id} | attributes
                table[count] = row
                count += 1

            if table != {}:
                frame = pd.DataFrame.from_dict(table, orient="index")
            else:
                frame = pd.DataFrame()

            self.resourceDictionary['ibm_is_subnet'] = frame

        # Build a vpc-id -> region lookup from subnets so each VPC gets its own
        # region rather than the last iteration variable from the subnets loop.
        vpc_region_map = {}
        if 'subnets' in data:
            for s in data['subnets']:
                vid = s.get('vpcId', '')
                reg = s.get('region', '')
                if vid and reg:
                    vpc_region_map[vid] = reg

        # Map vpcs to name, id, crn
        if 'vpcs' in data:
            count = 0
            table = {}
            vpcs = data['vpcs']

            for vpc in vpcs:
                name = vpc['name']
                id = vpc['id']
                # Prefer region declared directly on the VPC; fall back to the
                # region derived from the VPC's subnets.
                region = vpc.get('region') or vpc_region_map.get(id, '')
                attributes = {'name': name, 'id': id,
                              'crn': 'crn:v1:bluemix:public:vpc:' + region}
                row = {"id": id} | attributes
                table[count] = row
                count += 1

            if table != {}:
                frame = pd.DataFrame.from_dict(table, orient="index")
            else:
                frame = pd.DataFrame()

            self.resourceDictionary['ibm_is_vpc'] = frame

        return True


__all__ = [
    'Resources',
    'RESOURCE_DICTIONARY',
    'COMPUTE_RESOURCES',
    'NETWORK_RESOURCES',
    'STORAGE_RESOURCES',
    'DATABASE_RESOURCES',
    'SECURITY_RESOURCES',
    'CONTAINER_RESOURCES',
    'OBSERVABILITY_RESOURCES',
]

# Made with Bob
