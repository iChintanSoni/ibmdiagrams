# @file test_e2e_python_to_drawio.py
#
# End-to-end tests that verify the full Python → .drawio pipeline.
#
# Each test builds a diagram using the public Python API, lets the context
# manager write the .drawio XML file to a temporary directory, then parses
# the file and asserts on the output structure.
#
# Coverage:
#   - File is created at the expected path
#   - XML skeleton (mxfile / diagram / mxGraphModel / root / cell0 / cell1)
#   - Groups produce container cells (container=1 in style)
#   - Items produce vertex cells
#   - Labels are preserved (IBM renderer wraps them in bold HTML)
#   - All shapes carry a positive-dimension mxGeometry
#   - The `-` operator creates an undirected edge with valid source/target IDs
#   - The `>>` operator creates a directed edge (endArrow=block)
#   - The `<<` operator creates a directed edge pointing the other way
#   - Nested groups produce correct parent-child IDs in the XML
#   - IBM Cloud convenience classes (VPC / Subnet / VirtualServer)
#   - Multiple items inside a single group all appear in the output

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from ibmdiagrams import Diagram, Group, Item, Connector
from ibmdiagrams.ibmcloud.diagram import IBMDiagram
from ibmdiagrams.ibmcloud.groups import IBMCloud, VPC, Subnet
from ibmdiagrams.ibmcloud.compute import VirtualServer
from ibmdiagrams.ibmcloud.network import LoadBalancer


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _parse(output_dir: Path, filename: str) -> ET.Element:
    """Parse a .drawio file and return the <mxfile> root element."""
    filepath = output_dir / f"{filename}.drawio"
    assert filepath.exists(), f"Expected output file not found: {filepath}"
    return ET.parse(filepath).getroot()


def _root(mxfile: ET.Element) -> ET.Element:
    """Return the <root> element inside mxfile > diagram > mxGraphModel."""
    root = mxfile.find("./diagram/mxGraphModel/root")
    assert root is not None, "<root> element not found in diagram"
    return root


def _strip_html(text: str) -> str:
    """Remove HTML tags and strip whitespace from a label value."""
    return re.sub(r"<[^>]+>", "", text or "").strip()


def _all_cells(root: ET.Element) -> list[ET.Element]:
    """All <mxCell> children of <root>."""
    return root.findall("mxCell")


def _vertex_cells(root: ET.Element) -> list[ET.Element]:
    """All <mxCell> children of <root> with vertex='1'."""
    return [c for c in _all_cells(root) if c.get("vertex") == "1"]


def _container_cells(root: ET.Element) -> list[ET.Element]:
    """Group container cells: vertex=1 and container=1 in style."""
    return [c for c in _vertex_cells(root)
            if "container=1" in (c.get("style") or "")]


def _edge_cells(root: ET.Element) -> list[ET.Element]:
    """All edge <mxCell> elements (may be wrapped in <UserObject>)."""
    edges = [c for c in _all_cells(root) if c.get("edge") == "1"]
    for uo in root.findall("UserObject"):
        for c in uo.findall("mxCell"):
            if c.get("edge") == "1":
                edges.append(c)
    return edges


def _plain_label_values(root: ET.Element) -> set[str]:
    """Set of plain-text labels (HTML stripped) from all vertex cells."""
    return {_strip_html(c.get("value", "")) for c in _vertex_cells(root)} - {""}


def _cell_by_label(root: ET.Element, label: str) -> ET.Element | None:
    """Find the first mxCell whose plain-text value equals label."""
    for c in _vertex_cells(root):
        if _strip_html(c.get("value", "")) == label:
            return c
    return None


def _container_id_for_label(root: ET.Element, label: str) -> str | None:
    """
    Return the container cell ID for a group.

    Groups have two cells: a container (value='') and a label cell
    (id='{containerid}-label', parent='{containerid}').  Given the label
    text we find the label cell and return its parent (the container ID).
    """
    label_cell = _cell_by_label(root, label)
    if label_cell is None:
        return None
    return label_cell.get("parent")


def _shape_ids(root: ET.Element) -> set[str]:
    """All IDs of vertex cells excluding the two bootstrap cells."""
    return {c.get("id") for c in _vertex_cells(root)} - {"0", "1", None}


def _geometry(cell: ET.Element) -> ET.Element:
    geo = cell.find("mxGeometry")
    assert geo is not None, f"mxGeometry missing on cell id={cell.get('id')}"
    return geo


# ---------------------------------------------------------------------------
# 1. File creation
# ---------------------------------------------------------------------------

class TestFileCreation:
    def test_drawio_file_is_created(self, tmp_path):
        with Diagram(name="test", filename="test_creation", output=str(tmp_path)):
            with Group(label="G"):
                Item(label="I")

        assert (tmp_path / "test_creation.drawio").exists()

    def test_filename_defaults_to_name_for_ibm_diagram(self, tmp_path):
        with IBMDiagram(name="mydiagram", output=str(tmp_path)):
            with VPC("VPC"):
                VirtualServer("VSI")

        assert (tmp_path / "mydiagram.drawio").exists()


# ---------------------------------------------------------------------------
# 2. XML skeleton
# ---------------------------------------------------------------------------

class TestXMLSkeleton:
    def test_root_element_is_mxfile(self, tmp_path):
        with Diagram(name="t", filename="skel", output=str(tmp_path)):
            with Group(label="G"):
                Item(label="I")

        assert _parse(tmp_path, "skel").tag == "mxfile"

    def test_diagram_name_attribute(self, tmp_path):
        with Diagram(name="My Diagram", filename="named", output=str(tmp_path)):
            with Group(label="G"):
                Item(label="I")

        mxfile = _parse(tmp_path, "named")
        diagram = mxfile.find("diagram")
        assert diagram is not None
        assert diagram.get("name") == "My Diagram"

    def test_mxgraphmodel_and_root_present(self, tmp_path):
        with Diagram(name="t", filename="model", output=str(tmp_path)):
            with Group(label="G"):
                Item(label="I")

        mxfile = _parse(tmp_path, "model")
        assert mxfile.find("./diagram/mxGraphModel") is not None
        assert mxfile.find("./diagram/mxGraphModel/root") is not None

    def test_bootstrap_cells_0_and_1_always_present(self, tmp_path):
        with Diagram(name="t", filename="boot", output=str(tmp_path)):
            with Group(label="G"):
                Item(label="I")

        root = _root(_parse(tmp_path, "boot"))
        ids = {c.get("id") for c in _all_cells(root)}
        assert "0" in ids, "Bootstrap cell id=0 is missing"
        assert "1" in ids, "Bootstrap cell id=1 is missing"

    def test_cell_0_has_no_parent(self, tmp_path):
        with Diagram(name="t", filename="cell0", output=str(tmp_path)):
            with Group(label="G"):
                Item(label="I")

        root = _root(_parse(tmp_path, "cell0"))
        cell0 = next(c for c in _all_cells(root) if c.get("id") == "0")
        assert cell0.get("parent") is None

    def test_cell_1_parent_is_0(self, tmp_path):
        with Diagram(name="t", filename="cell1", output=str(tmp_path)):
            with Group(label="G"):
                Item(label="I")

        root = _root(_parse(tmp_path, "cell1"))
        cell1 = next(c for c in _all_cells(root) if c.get("id") == "1")
        assert cell1.get("parent") == "0"


# ---------------------------------------------------------------------------
# 3. Groups
# ---------------------------------------------------------------------------

class TestGroups:
    def test_group_produces_a_container_cell(self, tmp_path):
        with Diagram(name="t", filename="grp_container", output=str(tmp_path)):
            with Group(label="MyGroup"):
                Item(label="I")

        root = _root(_parse(tmp_path, "grp_container"))
        assert len(_container_cells(root)) >= 1

    def test_group_style_contains_container_flag(self, tmp_path):
        with Diagram(name="t", filename="grp_style", output=str(tmp_path)):
            with Group(label="MyGroup"):
                Item(label="I")

        root = _root(_parse(tmp_path, "grp_style"))
        containers = _container_cells(root)
        assert len(containers) >= 1, "No cell with container=1 in style found"

    def test_group_label_preserved(self, tmp_path):
        with Diagram(name="t", filename="grp_label", output=str(tmp_path)):
            with Group(label="ZoneGroup"):
                Item(label="I")

        root = _root(_parse(tmp_path, "grp_label"))
        assert "ZoneGroup" in _plain_label_values(root)

    def test_group_sublabel_preserved(self, tmp_path):
        with Diagram(name="t", filename="grp_sublabel", output=str(tmp_path)):
            with Group(label="VPCGroup", sublabel="10.0.0.0/16"):
                Item(label="I")

        root = _root(_parse(tmp_path, "grp_sublabel"))
        # Sublabel may be combined into the label value or on a separate cell
        all_values = " ".join(c.get("value", "") for c in _vertex_cells(root))
        assert "10.0.0.0/16" in all_values


# ---------------------------------------------------------------------------
# 4. Items
# ---------------------------------------------------------------------------

class TestItems:
    def test_item_produces_a_vertex_cell(self, tmp_path):
        with Diagram(name="t", filename="item_vertex", output=str(tmp_path)):
            with Group(label="G"):
                Item(label="Server")

        root = _root(_parse(tmp_path, "item_vertex"))
        assert len(_vertex_cells(root)) >= 2  # at least group + item

    def test_item_label_preserved(self, tmp_path):
        with Diagram(name="t", filename="item_label", output=str(tmp_path)):
            with Group(label="G"):
                Item(label="Database Node")

        root = _root(_parse(tmp_path, "item_label"))
        assert "Database Node" in _plain_label_values(root)

    def test_multiple_items_all_appear(self, tmp_path):
        with Diagram(name="t", filename="multi_items", output=str(tmp_path)):
            with Group(label="G"):
                Item(label="Alpha")
                Item(label="Beta")
                Item(label="Gamma")

        root = _root(_parse(tmp_path, "multi_items"))
        labels = _plain_label_values(root)
        assert {"Alpha", "Beta", "Gamma"}.issubset(labels)


# ---------------------------------------------------------------------------
# 5. Geometry
# ---------------------------------------------------------------------------

class TestGeometry:
    def test_all_shapes_have_mxgeometry(self, tmp_path):
        with Diagram(name="t", filename="geo", output=str(tmp_path)):
            with Group(label="G"):
                Item(label="I1")
                Item(label="I2")

        root = _root(_parse(tmp_path, "geo"))
        for cell in _vertex_cells(root):
            assert cell.find("mxGeometry") is not None, (
                f"mxGeometry missing on cell id={cell.get('id')}"
            )

    def test_shapes_have_positive_width_and_height(self, tmp_path):
        with Diagram(name="t", filename="geo_dims", output=str(tmp_path)):
            with Group(label="G"):
                Item(label="I")

        root = _root(_parse(tmp_path, "geo_dims"))
        for cell in _vertex_cells(root):
            geo = _geometry(cell)
            w = float(geo.get("width", 0))
            h = float(geo.get("height", 0))
            assert w > 0, f"Cell id={cell.get('id')} has width={w}"
            assert h > 0, f"Cell id={cell.get('id')} has height={h}"


# ---------------------------------------------------------------------------
# 6. Connectors
# ---------------------------------------------------------------------------

class TestConnectors:
    def test_minus_operator_creates_edge(self, tmp_path):
        with Diagram(name="t", filename="conn_edge", output=str(tmp_path)):
            with Group(label="G"):
                a = Item(label="A")
                b = Item(label="B")
            a - b

        root = _root(_parse(tmp_path, "conn_edge"))
        assert len(_edge_cells(root)) == 1

    def test_connector_source_and_target_are_valid_shape_ids(self, tmp_path):
        with Diagram(name="t", filename="conn_ids", output=str(tmp_path)):
            with Group(label="G"):
                a = Item(label="A")
                b = Item(label="B")
            a - b

        root = _root(_parse(tmp_path, "conn_ids"))
        ids = _shape_ids(root)
        edges = _edge_cells(root)
        assert len(edges) == 1
        assert edges[0].get("source") in ids, "Edge source ID not found among shapes"
        assert edges[0].get("target") in ids, "Edge target ID not found among shapes"

    def test_rshift_operator_creates_directed_edge(self, tmp_path):
        with Diagram(name="t", filename="conn_rshift", output=str(tmp_path)):
            with Group(label="G"):
                a = Item(label="A")
                b = Item(label="B")
            a >> b

        root = _root(_parse(tmp_path, "conn_rshift"))
        edges = _edge_cells(root)
        assert len(edges) == 1
        style = edges[0].get("style", "")
        assert "endArrow=block" in style, f"Expected endArrow=block in style, got: {style}"

    def test_lshift_operator_creates_directed_edge(self, tmp_path):
        with Diagram(name="t", filename="conn_lshift", output=str(tmp_path)):
            with Group(label="G"):
                a = Item(label="A")
                b = Item(label="B")
            a << b

        root = _root(_parse(tmp_path, "conn_lshift"))
        edges = _edge_cells(root)
        assert len(edges) == 1
        style = edges[0].get("style", "")
        assert "endArrow=block" in style, f"Expected endArrow=block in style, got: {style}"

    def test_connector_label_preserved(self, tmp_path):
        with Diagram(name="t", filename="conn_label", output=str(tmp_path)):
            with Group(label="G"):
                a = Item(label="A")
                b = Item(label="B")
            a - Connector(label="flows to") - b

        root = _root(_parse(tmp_path, "conn_label"))
        user_objects = root.findall("UserObject")
        labels = {uo.get("label") for uo in user_objects}
        assert "flows to" in labels

    def test_multiple_connectors_all_appear(self, tmp_path):
        with Diagram(name="t", filename="conn_multi", output=str(tmp_path)):
            with Group(label="G"):
                a = Item(label="A")
                b = Item(label="B")
                c = Item(label="C")
            a - b
            b - c

        root = _root(_parse(tmp_path, "conn_multi"))
        assert len(_edge_cells(root)) == 2

    def test_connector_arrow_types_mapped(self, tmp_path):
        with Diagram(name="t", filename="conn_arrows", output=str(tmp_path)):
            with Group(label="G"):
                a = Item(label="A")
                b = Item(label="B")
            a - Connector(startarrow="CIRCLE", endarrow="DIAMOND") - b

        root = _root(_parse(tmp_path, "conn_arrows"))
        edges = _edge_cells(root)
        assert len(edges) == 1
        style = edges[0].get("style", "")
        assert "startArrow=oval" in style
        assert "endArrow=diamond" in style


# ---------------------------------------------------------------------------
# 7. Nesting
# ---------------------------------------------------------------------------

class TestNesting:
    def test_nested_group_parent_id_matches_outer_group_id(self, tmp_path):
        with Diagram(name="t", filename="nested", output=str(tmp_path)):
            with Group(label="Outer"):
                with Group(label="Inner"):
                    Item(label="I")

        root = _root(_parse(tmp_path, "nested"))
        outer_id = _container_id_for_label(root, "Outer")
        inner_id = _container_id_for_label(root, "Inner")
        assert outer_id is not None, "'Outer' group label cell not found"
        assert inner_id is not None, "'Inner' group label cell not found"

        # The inner container cell's parent should be the outer container
        inner_container = next(
            (c for c in _all_cells(root) if c.get("id") == inner_id), None
        )
        assert inner_container is not None
        assert inner_container.get("parent") == outer_id, (
            f"Inner container parent={inner_container.get('parent')!r} "
            f"should equal outer container id={outer_id!r}"
        )

    def test_item_parent_id_matches_containing_group(self, tmp_path):
        with Diagram(name="t", filename="item_parent", output=str(tmp_path)):
            with Group(label="Container"):
                Item(label="Child")

        root = _root(_parse(tmp_path, "item_parent"))
        container_id = _container_id_for_label(root, "Container")
        assert container_id is not None, "'Container' label cell not found"

        child_cell = _cell_by_label(root, "Child")
        assert child_cell is not None, "'Child' item cell not found"
        assert child_cell.get("parent") == container_id, (
            f"Item parent={child_cell.get('parent')!r} "
            f"should equal container id={container_id!r}"
        )


# ---------------------------------------------------------------------------
# 8. IBM Cloud convenience classes
# ---------------------------------------------------------------------------

class TestIBMCloudClasses:
    def test_vpc_and_virtual_server_produce_output(self, tmp_path):
        with IBMDiagram(name="ibm_basic", output=str(tmp_path)):
            with VPC("My VPC"):
                VirtualServer("VSI-1")

        root = _root(_parse(tmp_path, "ibm_basic"))
        labels = _plain_label_values(root)
        assert "My VPC" in labels
        assert "VSI-1" in labels

    def test_ibmcloud_subnet_nesting(self, tmp_path):
        with IBMDiagram(name="ibm_nested", output=str(tmp_path)):
            with IBMCloud("IBM Cloud"):
                with VPC("VPC"):
                    with Subnet("Subnet A"):
                        VirtualServer("VSI")

        root = _root(_parse(tmp_path, "ibm_nested"))
        labels = _plain_label_values(root)
        assert {"IBM Cloud", "VPC", "Subnet A", "VSI"}.issubset(labels)

    def test_ibm_connector_between_items(self, tmp_path):
        with IBMDiagram(name="ibm_conn", output=str(tmp_path)):
            with VPC("VPC"):
                with Subnet("Subnet"):
                    lb = LoadBalancer("LB")
                    vsi = VirtualServer("VSI")
            lb >> vsi

        root = _root(_parse(tmp_path, "ibm_conn"))
        edges = _edge_cells(root)
        assert len(edges) == 1
        ids = _shape_ids(root)
        assert edges[0].get("source") in ids
        assert edges[0].get("target") in ids

    def test_ibm_diagram_all_shapes_have_positive_geometry(self, tmp_path):
        with IBMDiagram(name="ibm_geo", output=str(tmp_path)):
            with IBMCloud("IBM Cloud"):
                with VPC("VPC"):
                    with Subnet("Subnet"):
                        VirtualServer("VSI-1")
                        VirtualServer("VSI-2")

        root = _root(_parse(tmp_path, "ibm_geo"))
        for cell in _vertex_cells(root):
            geo = _geometry(cell)
            assert float(geo.get("width", 0)) > 0
            assert float(geo.get("height", 0)) > 0

    def test_direction_tb_produces_output(self, tmp_path):
        with IBMDiagram(name="tb_diag", output=str(tmp_path), direction="TB"):
            with VPC("VPC"):
                with Subnet("S"):
                    VirtualServer("VSI")

        root = _root(_parse(tmp_path, "tb_diag"))
        labels = _plain_label_values(root)
        assert "VPC" in labels

    def test_ibm_nested_group_parent_child_relationship(self, tmp_path):
        with IBMDiagram(name="ibm_nesting", output=str(tmp_path)):
            with VPC("MyVPC"):
                with Subnet("MySubnet"):
                    VirtualServer("MyVSI")

        root = _root(_parse(tmp_path, "ibm_nesting"))
        vpc_id = _container_id_for_label(root, "MyVPC")
        subnet_id = _container_id_for_label(root, "MySubnet")
        assert vpc_id is not None
        assert subnet_id is not None

        subnet_container = next(
            (c for c in _all_cells(root) if c.get("id") == subnet_id), None
        )
        assert subnet_container is not None
        assert subnet_container.get("parent") == vpc_id


# ---------------------------------------------------------------------------
# 9. Font name is propagated
#
# The library only supports IBM Plex Sans variants (see FontNames enum).
# Unsupported font strings are silently ignored and IBM Plex Sans is used.
# ---------------------------------------------------------------------------

class TestFontPropagation:
    def test_default_font_ibm_plex_sans_appears_in_styles(self, tmp_path):
        with Diagram(name="t", filename="font_default", output=str(tmp_path)):
            with Group(label="G"):
                Item(label="I")

        root = _root(_parse(tmp_path, "font_default"))
        all_styles = [c.get("style", "") for c in _vertex_cells(root)]
        assert any("fontFamily=IBM Plex Sans" in s for s in all_styles), (
            "Expected 'fontFamily=IBM Plex Sans' in at least one shape style."
        )

    def test_valid_ibm_font_variant_propagates(self, tmp_path):
        # IBM Plex Sans JP is a valid variant in the FontNames enum
        with Diagram(name="t", filename="font_variant", output=str(tmp_path),
                     font="IBM Plex Sans JP"):
            with Group(label="G"):
                Item(label="I")

        root = _root(_parse(tmp_path, "font_variant"))
        all_styles = [c.get("style", "") for c in _vertex_cells(root)]
        assert any("IBM Plex Sans JP" in s for s in all_styles), (
            "Expected 'IBM Plex Sans JP' in at least one shape style."
        )
