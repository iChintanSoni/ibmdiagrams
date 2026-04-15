"""
Tests for file I/O and JSON parse error handling.

Three locations previously had no error handling around open() / json.loads():
  - opsjson.py  loadJSON()  — plain open + json_load, no try/except
  - opsjson.py  loadYAML()  — plain open + yaml_load, no try/except
  - resources.py loadJSON() — plain open + json_load, no try/except
  - resources.py loadResources() — plain open + json_load, no try/except

Without error handling a missing file, permission error, or malformed JSON
produces a raw Python traceback instead of a user-friendly message.

Fix: wrap all open() and json/yaml parse calls with try/except that calls
common.printInvalidFile() and then exits (opsjson) or returns False
(resources), matching the existing error-handling style in each module.
"""

import json
import pytest
from unittest.mock import MagicMock, patch, mock_open

from ibmdiagrams.ibmbase.opsjson import OpsJson
from ibmdiagrams.ibmbase.resources import Resources


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_opsjson():
    common = MagicMock()
    common.getInputFile.return_value = "dummy.json"
    obj = OpsJson.__new__(OpsJson)
    obj.common = common
    obj.data = {}
    obj.icons = MagicMock()
    return obj


def make_resources():
    common = MagicMock()
    common.getInputFile.return_value = "dummy.json"
    r = Resources.__new__(Resources)
    r.common = common
    r.resourceDictionary = {}
    return r


# ---------------------------------------------------------------------------
# OpsJson.loadJSON
# ---------------------------------------------------------------------------

class TestOpsJsonLoadJSONErrors:

    def test_missing_file_calls_printInvalidFile_and_exits(self):
        """OSError (e.g. FileNotFoundError) must print an error and call exit()."""
        obj = make_opsjson()
        with patch("builtins.open", side_effect=FileNotFoundError("no such file")), \
             pytest.raises(SystemExit):
            obj.loadJSON()
        obj.common.printInvalidFile.assert_called_once_with("dummy.json")

    def test_permission_error_calls_printInvalidFile_and_exits(self):
        """PermissionError must print an error and call exit()."""
        obj = make_opsjson()
        with patch("builtins.open", side_effect=PermissionError("access denied")), \
             pytest.raises(SystemExit):
            obj.loadJSON()
        obj.common.printInvalidFile.assert_called_once_with("dummy.json")

    def test_malformed_json_calls_printInvalidFile_and_exits(self):
        """A JSON parse error must print an error and call exit()."""
        obj = make_opsjson()
        with patch("builtins.open", mock_open(read_data="{ this is not json }")), \
             pytest.raises(SystemExit):
            obj.loadJSON()
        obj.common.printInvalidFile.assert_called_once_with("dummy.json")

    def test_valid_json_without_vpcs_calls_printMissingVPCs(self):
        """A valid JSON file missing the 'vpcs' key should call printMissingVPCs."""
        obj = make_opsjson()
        with patch("builtins.open", mock_open(read_data='{"subnets": []}')), \
             pytest.raises(SystemExit):
            obj.loadJSON()
        obj.common.printMissingVPCs.assert_called_once()
        # printInvalidFile must NOT have been called — this is a schema error, not I/O
        obj.common.printInvalidFile.assert_not_called()


# ---------------------------------------------------------------------------
# OpsJson.loadYAML
# ---------------------------------------------------------------------------

class TestOpsJsonLoadYAMLErrors:

    def test_missing_file_calls_printInvalidFile_and_exits(self):
        """OSError on YAML load must print an error and exit."""
        obj = make_opsjson()
        with patch("builtins.open", side_effect=FileNotFoundError("no such file")), \
             pytest.raises(SystemExit):
            obj.loadYAML()
        obj.common.printInvalidFile.assert_called_once_with("dummy.json")

    def test_malformed_yaml_calls_printInvalidFile_and_exits(self):
        """A YAML parse error must print an error and exit."""
        import yaml
        obj = make_opsjson()
        with patch("builtins.open", mock_open(read_data="{")), \
             patch("ibmdiagrams.ibmbase.opsjson.yaml_load",
                   side_effect=yaml.YAMLError("bad yaml")), \
             pytest.raises(SystemExit):
            obj.loadYAML()
        obj.common.printInvalidFile.assert_called_once_with("dummy.json")


# ---------------------------------------------------------------------------
# Resources.loadJSON
# ---------------------------------------------------------------------------

class TestResourcesLoadJSONErrors:

    def _make_with_file(self):
        r = make_resources()
        # Bypass the os.path.isfile() early-return
        with patch("ibmdiagrams.ibmbase.resources.os.path.isfile", return_value=True):
            return r

    def test_missing_file_returns_false_and_prints_error(self):
        """OSError must call printInvalidFile and return False."""
        r = make_resources()
        with patch("ibmdiagrams.ibmbase.resources.os.path.isfile", return_value=True), \
             patch("builtins.open", side_effect=FileNotFoundError("no such file")):
            result = r.loadJSON()
        assert result is False
        r.common.printInvalidFile.assert_called_once()

    def test_malformed_json_returns_false_and_prints_error(self):
        """A JSON parse error must call printInvalidFile and return False."""
        r = make_resources()
        with patch("ibmdiagrams.ibmbase.resources.os.path.isfile", return_value=True), \
             patch("builtins.open", mock_open(read_data="{ bad json }")):
            result = r.loadJSON()
        assert result is False
        r.common.printInvalidFile.assert_called_once()

    def test_nonexistent_file_returns_false_without_error_message(self):
        """When os.path.isfile returns False, loadJSON returns False silently."""
        r = make_resources()
        with patch("ibmdiagrams.ibmbase.resources.os.path.isfile", return_value=False):
            result = r.loadJSON()
        assert result is False
        r.common.printInvalidFile.assert_not_called()


# ---------------------------------------------------------------------------
# Resources.loadResources
# ---------------------------------------------------------------------------

class TestResourcesLoadResourcesErrors:

    def test_missing_file_returns_false_and_prints_error(self):
        """OSError must call printInvalidFile and return False."""
        r = make_resources()
        with patch("ibmdiagrams.ibmbase.resources.os.path.isfile", return_value=True), \
             patch("builtins.open", side_effect=PermissionError("access denied")):
            result = r.loadResources()
        assert result is False
        r.common.printInvalidFile.assert_called_once()

    def test_malformed_json_returns_false_and_prints_error(self):
        """A JSON parse error must call printInvalidFile and return False."""
        r = make_resources()
        with patch("ibmdiagrams.ibmbase.resources.os.path.isfile", return_value=True), \
             patch("builtins.open", mock_open(read_data="not json at all")):
            result = r.loadResources()
        assert result is False
        r.common.printInvalidFile.assert_called_once()
