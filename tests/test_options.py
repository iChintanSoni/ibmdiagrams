"""
Tests for options.py getter/setter correctness.

Focus: getInputFolder() was returning self.outputFile (copy-paste error)
instead of self.inputFolder, causing any caller that reads the input folder
to silently receive the output file path instead.
"""

import pytest
from ibmdiagrams.ibmbase.options import Options


class TestGetInputFolder:

    def test_get_input_folder_returns_input_folder_not_output_file(self):
        """getInputFolder() must return the inputFolder attribute, not outputFile."""
        opts = Options()
        opts.setInputFile("/data/input.json")
        opts.inputFolder = "/data/inputs/"
        opts.setOutputFile("/data/output.xml")

        assert opts.getInputFolder() == "/data/inputs/", (
            "getInputFolder() returned the wrong value — "
            f"got {opts.getInputFolder()!r}, expected '/data/inputs/'"
        )

    def test_get_input_folder_does_not_return_output_file(self):
        """getInputFolder() must never return the output file path."""
        opts = Options()
        opts.setOutputFile("/some/output/diagram.xml")
        opts.inputFolder = "/some/input/folder/"

        result = opts.getInputFolder()
        assert result != "/some/output/diagram.xml", (
            "getInputFolder() returned the output file path — this is the original bug"
        )

    def test_set_and_get_input_folder_roundtrip(self):
        """setInputFolder / getInputFolder must be a consistent round-trip."""
        opts = Options()
        opts.setInputFolder("/my/input/folder")
        assert opts.getInputFolder() == "/my/input/folder"

    def test_input_folder_and_output_file_are_independent(self):
        """Changing outputFile must not affect getInputFolder(), and vice versa."""
        opts = Options()
        opts.setInputFolder("/inputs/")
        opts.setOutputFile("/outputs/diagram.xml")

        # Changing output must not touch input folder
        opts.setOutputFile("/other/diagram.xml")
        assert opts.getInputFolder() == "/inputs/"

        # Changing input folder must not touch output file
        opts.setInputFolder("/other-inputs/")
        assert opts.getOutputFile() == "/other/diagram.xml"

    def test_default_input_folder_is_empty_string(self):
        """Fresh Options instance must have an empty input folder by default."""
        opts = Options()
        assert opts.getInputFolder() == ""
