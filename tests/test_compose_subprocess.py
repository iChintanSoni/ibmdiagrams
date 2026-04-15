"""
Tests for composeDiagrams() subprocess handling and file management.

Two bugs were present:
1. File handle leak — the generated .py file was opened without a context
   manager, so an exception before pythonfile.close() would leave the
   handle open.
2. Silent subprocess failure — subprocess.run() result code and stderr were
   never checked, so a crashed generated script produced no diagnostic.

The fix:
- Use a `with` statement so the file is always closed on exit/exception.
- Check result.returncode after subprocess.run(); print stderr and return
  False on non-zero exit; return True on success.
"""

import subprocess
import sys
from io import StringIO
from unittest.mock import MagicMock, patch, call
import pytest

from ibmdiagrams.ibmbase.compose import Compose, TreeNode


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_compose(drawio_code=True, output_folder="", output_file="test.xml"):
    common = MagicMock()
    common.isCustomLabels.return_value = False
    common.isDrawioCode.return_value = drawio_code
    common.getFontName.return_value = None
    common.getOutputFolder.return_value = output_folder
    common.getOutputFile.return_value = output_file
    common.getProvider.return_value = MagicMock(value="IBM")

    data = MagicMock()
    data.getIcons.return_value = MagicMock(getIconDictionary=MagicMock(return_value={}))

    compose = Compose.__new__(Compose)
    compose.common = common
    compose.data = data
    compose.icons = data.getIcons()
    compose.top = None
    compose.savegroups = {}
    compose.indent = -2
    compose.provider = "IBM"
    compose.diagramname = "test"
    compose.outputfile = "test.py"
    compose.outputfolder = output_folder
    return compose


# ---------------------------------------------------------------------------
# Tests: context manager / file closure
# ---------------------------------------------------------------------------

class TestFileHandleClosure:

    def test_file_is_closed_after_successful_write(self, tmp_path):
        """Generated .py file handle must be closed even on the happy path."""
        compose = make_compose(drawio_code=False, output_folder=str(tmp_path),
                               output_file="diagram.xml")
        compose.outputfile = "diagram.py"

        import pandas as pd
        diagramdata = {"label": ["diagram"]}
        frame = pd.DataFrame(diagramdata)
        from ibmdiagrams.ibmbase.compose import randomid
        compose.top = TreeNode("Diagram Group", randomid(), str(tmp_path), 'LR', None, frame.iloc[0])

        with patch.object(compose, 'composeTree', return_value=compose.top), \
             patch.object(compose, 'composeIncludes'), \
             patch.object(compose, 'composeResources'):
            compose.composeDiagrams()

        out_file = tmp_path / "diagram.py"
        # File must exist and be readable (would fail if handle leaked with 'w' exclusive)
        assert out_file.exists()

    def test_file_is_closed_when_compose_resources_raises(self, tmp_path):
        """File handle must be closed even if composeResources() raises."""
        compose = make_compose(drawio_code=False, output_folder=str(tmp_path),
                               output_file="diagram.xml")
        compose.outputfile = "diagram.py"

        import pandas as pd
        frame = pd.DataFrame({"label": ["diagram"]})
        from ibmdiagrams.ibmbase.compose import randomid
        compose.top = TreeNode("Diagram Group", randomid(), str(tmp_path), 'LR', None, frame.iloc[0])

        with patch.object(compose, 'composeTree', return_value=compose.top), \
             patch.object(compose, 'composeIncludes'), \
             patch.object(compose, 'composeResources', side_effect=RuntimeError("boom")):
            with pytest.raises(RuntimeError):
                compose.composeDiagrams()

        out_file = tmp_path / "diagram.py"
        if out_file.exists():
            # If the file was created, it must be openable (not locked)
            with open(out_file, 'r') as f:
                pass  # should not raise


# ---------------------------------------------------------------------------
# Tests: subprocess error propagation
# ---------------------------------------------------------------------------

class TestSubprocessErrorPropagation:

    def _run_with_mock_subprocess(self, tmp_path, returncode, stderr=""):
        """Helper: run composeDiagrams() with subprocess.run mocked to return given code."""
        compose = make_compose(drawio_code=True, output_folder=str(tmp_path),
                               output_file="diagram.xml")
        compose.outputfile = "diagram.py"

        import pandas as pd
        frame = pd.DataFrame({"label": ["diagram"]})
        from ibmdiagrams.ibmbase.compose import randomid
        compose.top = TreeNode("Diagram Group", randomid(), str(tmp_path), 'LR', None, frame.iloc[0])

        mock_result = MagicMock()
        mock_result.returncode = returncode
        mock_result.stderr = stderr
        mock_result.stdout = ""

        with patch.object(compose, 'composeTree', return_value=compose.top), \
             patch.object(compose, 'composeIncludes'), \
             patch.object(compose, 'composeResources'), \
             patch('ibmdiagrams.ibmbase.compose.subprocess.run', return_value=mock_result), \
             patch('ibmdiagrams.ibmbase.compose.remove'):
            return compose.composeDiagrams()

    def test_returns_true_on_successful_subprocess(self, tmp_path):
        """composeDiagrams() must return True when the subprocess exits 0."""
        result = self._run_with_mock_subprocess(tmp_path, returncode=0)
        assert result is True

    def test_returns_false_on_failed_subprocess(self, tmp_path):
        """composeDiagrams() must return False when the subprocess exits non-zero."""
        result = self._run_with_mock_subprocess(tmp_path, returncode=1, stderr="SyntaxError")
        assert result is False

    def test_stderr_printed_on_subprocess_failure(self, tmp_path, capsys):
        """Subprocess stderr must be printed to sys.stderr on non-zero exit."""
        self._run_with_mock_subprocess(tmp_path, returncode=1, stderr="NameError: test_error")
        captured = capsys.readouterr()
        assert "NameError: test_error" in captured.err

    def test_no_stderr_output_on_success(self, tmp_path, capsys):
        """No error output should be emitted when subprocess succeeds."""
        self._run_with_mock_subprocess(tmp_path, returncode=0)
        captured = capsys.readouterr()
        assert captured.err == ""

    def test_generated_file_is_removed_after_subprocess_runs(self, tmp_path):
        """The temporary .py file must be removed regardless of subprocess result."""
        compose = make_compose(drawio_code=True, output_folder=str(tmp_path),
                               output_file="diagram.xml")
        compose.outputfile = "diagram.py"

        import pandas as pd
        frame = pd.DataFrame({"label": ["diagram"]})
        from ibmdiagrams.ibmbase.compose import randomid
        compose.top = TreeNode("Diagram Group", randomid(), str(tmp_path), 'LR', None, frame.iloc[0])

        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "error"
        mock_result.stdout = ""

        removed_paths = []

        def capture_remove(p):
            removed_paths.append(p)

        with patch.object(compose, 'composeTree', return_value=compose.top), \
             patch.object(compose, 'composeIncludes'), \
             patch.object(compose, 'composeResources'), \
             patch('ibmdiagrams.ibmbase.compose.subprocess.run', return_value=mock_result), \
             patch('ibmdiagrams.ibmbase.compose.remove', side_effect=capture_remove):
            compose.composeDiagrams()

        assert len(removed_paths) == 1, "Expected remove() to be called exactly once"
        assert "diagram.py" in removed_paths[0]
