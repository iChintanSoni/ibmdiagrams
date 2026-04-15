"""
Tests for path traversal prevention in elements.py dumpXML().

Bug: `file` was joined directly with `folder` without stripping directory
components, so a filename like '../../etc/evil.xml' would resolve outside
the intended output folder and write there.

Fix: use os.path.basename() to strip any directory portion from `file`
before joining with `folder`, then verify the resolved path stays within
the base folder.
"""

import os
import pytest
from xml.etree import ElementTree as ET
from unittest.mock import patch, MagicMock

from ibmdiagrams.ibmbase.elements import Elements


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

HEADER = {
    "header": {"version": "21.0", "host": "test"},
    "graph": {"dx": "0", "dy": "0", "grid": "0", "gridSize": "10",
              "guides": "0", "tooltips": "0", "connect": "0",
              "arrows": "0", "fold": "0", "page": "0",
              "pageScale": "1", "pageWidth": "1654",
              "pageHeight": "1169", "math": "0", "shadow": "0"},
    "cell0": {"id": "0"},
    "cell1": {"id": "1", "parent": "0"},
}


def make_elements():
    e = Elements(HEADER)
    e.addDiagram(HEADER)
    return e


# ---------------------------------------------------------------------------
# Tests: traversal attempt raises ValueError
# ---------------------------------------------------------------------------

class TestPathTraversalPrevention:

    def test_traversal_with_dotdot_is_neutralised(self, tmp_path):
        """
        A filename containing '../' must be written INSIDE the output folder,
        not outside it.  os.path.basename('../../evil.xml') == 'evil.xml', so
        the file lands at <folder>/evil.xml rather than escaping.
        """
        e = make_elements()
        e.dumpXML("../../evil.xml", str(tmp_path))
        # File written safely inside tmp_path — directory traversal neutralised
        assert (tmp_path / "evil.xml").exists()
        # Confirm nothing was written two levels up
        parent_evil = tmp_path.parent.parent / "evil.xml"
        assert not parent_evil.exists()

    def test_traversal_with_absolute_path_is_neutralised(self, tmp_path):
        """An absolute path as filename must be stripped to basename (no traversal)."""
        e = make_elements()
        # os.path.basename("/etc/passwd.xml") == "passwd.xml", stays inside tmp_path
        e.dumpXML("/etc/passwd.xml", str(tmp_path))
        # The file written should be inside tmp_path, named 'passwd.xml'
        assert (tmp_path / "passwd.xml").exists()
        # /etc/passwd.xml must NOT have been created
        assert not os.path.exists("/etc/passwd.xml")

    def test_traversal_with_nested_dotdot_is_neutralised(self, tmp_path):
        """Deeply nested '../' sequences are neutralised by basename extraction."""
        e = make_elements()
        # basename("subdir/../../evil.xml") == "evil.xml"
        e.dumpXML("subdir/../../evil.xml", str(tmp_path))
        assert (tmp_path / "evil.xml").exists()

    def test_benign_filename_writes_inside_folder(self, tmp_path):
        """A plain filename must write the file inside the output folder."""
        e = make_elements()
        e.dumpXML("diagram.xml", str(tmp_path))
        assert (tmp_path / "diagram.xml").exists()

    def test_filename_with_spaces_stripped_and_written(self, tmp_path):
        """Spaces in filenames are stripped (existing behaviour) and file writes safely."""
        e = make_elements()
        e.dumpXML("my diagram.xml", str(tmp_path))
        assert (tmp_path / "mydiagram.xml").exists()

    def test_written_file_is_valid_xml(self, tmp_path):
        """The file written by dumpXML must be parseable XML."""
        e = make_elements()
        e.dumpXML("output.xml", str(tmp_path))
        tree = ET.parse(str(tmp_path / "output.xml"))
        assert tree.getroot().tag == "mxfile"

    def test_output_folder_created_if_missing(self, tmp_path):
        """dumpXML must create the output folder if it does not exist."""
        subfolder = tmp_path / "subdir" / "nested"
        e = make_elements()
        e.dumpXML("output.xml", str(subfolder))
        assert (subfolder / "output.xml").exists()
