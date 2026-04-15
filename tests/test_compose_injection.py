"""
Tests for code injection prevention in compose.py.

The composeResources method generates Python source code from user-supplied data
(labels, sublabels, output paths, direction, fontname). All of these must be
safely escaped with repr() so that malicious input cannot inject arbitrary code
into the generated file that is then executed via subprocess.

The invariant we test: every argument passed to generated function/class calls
must be a string literal (ast.Constant with str value). If an argument contains
actual Python expressions (imports, function calls, etc.) that is injection.
"""

import io
import ast
import pandas as pd
import pytest
from unittest.mock import MagicMock

from ibmdiagrams.ibmbase.compose import Compose, TreeNode


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_compose(custom_labels=False, drawio_code=True, output_folder="", output_file="test.xml"):
    """Return a minimally-configured Compose instance with mocked common/data."""
    common = MagicMock()
    common.isCustomLabels.return_value = custom_labels
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


def make_node(name, label, sublabel=None, output=None, direction="LR", fontname=None):
    """Return a TreeNode whose data series contains the given label/sublabel."""
    row_data = {"label": label, "id": "test-id-001"}
    if sublabel is not None:
        row_data["sublabel"] = sublabel
    df = pd.DataFrame([row_data])
    node = TreeNode(name, "test-id-001", output, direction, fontname, df.iloc[0])
    return node


def generated_lines(compose, node, use_custom_label=True):
    """Run composeResources and return the generated lines as a list."""
    buf = io.StringIO()
    compose.composeResources(node, use_custom_label, buf)
    return buf.getvalue().splitlines()


def parse_group_line(line):
    """
    Parse a group code line (a `with` statement) into an AST.
    Appends a minimal body so the with-statement is syntactically complete.
    """
    # Strip leading whitespace, keep trailing colon
    stmt = line.strip()
    assert stmt.endswith(":"), f"Group line must end with ':': {stmt!r}"
    # Wrap in a complete with-block so ast.parse can handle it
    return ast.parse(stmt + "\n    pass")


def parse_icon_line(line):
    """Parse an icon code line (a standalone expression statement) into an AST."""
    return ast.parse(line.strip())


def all_call_args_are_string_literals(tree):
    """
    Return True iff every argument (positional or keyword value) of every
    Call node in the AST is a plain string constant (ast.Constant with str value).

    This is the key security invariant: user data may only appear as string
    literals, never as arbitrary Python expressions.
    """
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            for arg in node.args:
                if not (isinstance(arg, ast.Constant) and isinstance(arg.value, str)):
                    return False
            for kw in node.keywords:
                if not (isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str)):
                    return False
    return True


# ---------------------------------------------------------------------------
# Group nodes
# ---------------------------------------------------------------------------

class TestGroupNodeInjection:
    """Malicious content in group node fields must be safely escaped."""

    def test_label_with_single_quote_is_escaped(self):
        """A label containing a single quote must produce a valid, safe with-statement."""
        compose = make_compose(custom_labels=False)
        node = make_node("VPC Group", "it's a label")
        lines = generated_lines(compose, node)
        assert lines, "Expected at least one output line"
        tree = parse_group_line(lines[0])
        assert all_call_args_are_string_literals(tree), \
            "All call args must be string literals — no injected expressions"

    def test_label_injection_attempt_is_neutralised(self):
        """Injection payload in label must be rendered as a string literal, not executable code."""
        payload = "x'); import os; os.system('id')  #"
        compose = make_compose(custom_labels=False)
        node = make_node("VPC Group", payload)
        lines = generated_lines(compose, node)
        tree = parse_group_line(lines[0])
        assert all_call_args_are_string_literals(tree), \
            "Injection payload must only appear as a string literal in the AST"
        # Confirm no import statements were injected at module level
        for n in ast.walk(tree):
            assert not isinstance(n, (ast.Import, ast.ImportFrom)), \
                "No import statements should be injected"

    def test_sublabel_injection_attempt_is_neutralised(self):
        """Injection payload in sublabel must be rendered as a string literal."""
        payload = "x', __import__('os').system('id'), '"
        compose = make_compose(custom_labels=False)
        node = make_node("VPC Group", "safe-label", sublabel=payload)
        lines = generated_lines(compose, node)
        tree = parse_group_line(lines[0])
        assert all_call_args_are_string_literals(tree)

    def test_output_path_injection_is_neutralised(self):
        """Injection payload in output path must be escaped."""
        payload = "/tmp/x'); os.system('id'); open('/tmp/x"
        compose = make_compose(custom_labels=False)
        node = make_node("VPC Group", "label", output=payload)
        lines = generated_lines(compose, node)
        tree = parse_group_line(lines[0])
        assert all_call_args_are_string_literals(tree)

    def test_direction_injection_is_neutralised(self):
        """Injection payload in direction must be escaped."""
        payload = "TB'); os.system('id'); x=('x"
        compose = make_compose(custom_labels=False)
        node = make_node("VPC Group", "label", direction=payload)
        lines = generated_lines(compose, node)
        tree = parse_group_line(lines[0])
        assert all_call_args_are_string_literals(tree)

    def test_fontname_injection_is_neutralised(self):
        """Injection payload in fontname must be escaped."""
        payload = "Arial'); import subprocess; subprocess.call(['id']); x=('x"
        compose = make_compose(custom_labels=False)
        node = make_node("VPC Group", "label", fontname=payload)
        lines = generated_lines(compose, node)
        tree = parse_group_line(lines[0])
        assert all_call_args_are_string_literals(tree)
        for n in ast.walk(tree):
            assert not isinstance(n, (ast.Import, ast.ImportFrom))

    def test_benign_label_is_preserved(self):
        """A normal label value must appear correctly inside the generated code."""
        compose = make_compose(custom_labels=False)
        node = make_node("VPC Group", "my-vpc-01")
        lines = generated_lines(compose, node)
        assert any("my-vpc-01" in line for line in lines)

    def test_label_with_backslash_is_escaped(self):
        """Backslashes in labels must be properly escaped so the generated code is valid."""
        compose = make_compose(custom_labels=False)
        node = make_node("VPC Group", r"C:\Users\test")
        lines = generated_lines(compose, node)
        tree = parse_group_line(lines[0])
        assert all_call_args_are_string_literals(tree)
        # The actual string value must round-trip correctly
        call_node = next(n for n in ast.walk(tree) if isinstance(n, ast.Call))
        assert call_node.args[0].value == r"C:\Users\test"

    def test_label_with_newline_is_escaped(self):
        """Newline in label must be escaped so it doesn't break the generated line."""
        compose = make_compose(custom_labels=False)
        node = make_node("VPC Group", "line1\nline2")
        lines = generated_lines(compose, node)
        # Must still be a single line ending in ':'
        assert len(lines) == 1
        tree = parse_group_line(lines[0])
        assert all_call_args_are_string_literals(tree)

    def test_label_with_double_quote_is_escaped(self):
        """Double quotes in labels must produce valid, safe Python."""
        compose = make_compose(custom_labels=False)
        node = make_node("VPC Group", 'label "with" quotes')
        lines = generated_lines(compose, node)
        tree = parse_group_line(lines[0])
        assert all_call_args_are_string_literals(tree)


# ---------------------------------------------------------------------------
# Icon nodes
# ---------------------------------------------------------------------------

class TestIconNodeInjection:
    """Malicious content in icon node fields must be safely escaped."""

    def test_icon_label_injection_is_neutralised(self):
        """Injection in icon label must be rendered as a string literal, not executable code."""
        payload = "x', __import__('os').system('id'), '"
        compose = make_compose(custom_labels=False)
        node = make_node("VirtualServer Icon", payload)
        lines = generated_lines(compose, node)
        tree = parse_icon_line(lines[0])
        assert all_call_args_are_string_literals(tree), \
            "Injection payload must only appear as a string literal in the AST"

    def test_icon_sublabel_injection_is_neutralised(self):
        """Injection in icon sublabel must be rendered as a string literal."""
        payload = "x'); __import__('os').system('id')  #"
        compose = make_compose(custom_labels=False)
        node = make_node("VirtualServer Icon", "label", sublabel=payload)
        lines = generated_lines(compose, node)
        tree = parse_icon_line(lines[0])
        assert all_call_args_are_string_literals(tree)

    def test_icon_benign_label_preserved(self):
        """A normal icon label must appear correctly in the generated code."""
        compose = make_compose(custom_labels=False)
        node = make_node("VirtualServer Icon", "my-server-01")
        lines = generated_lines(compose, node)
        assert any("my-server-01" in line for line in lines)

    def test_icon_label_with_single_quote_is_escaped(self):
        """Single quotes in icon labels must produce valid, safe Python."""
        compose = make_compose(custom_labels=False)
        node = make_node("VirtualServer Icon", "server's label")
        lines = generated_lines(compose, node)
        tree = parse_icon_line(lines[0])
        assert all_call_args_are_string_literals(tree)

    def test_icon_label_with_double_quote_is_escaped(self):
        """Double-quote characters in labels must not break out of string literals."""
        compose = make_compose(custom_labels=False)
        node = make_node("VirtualServer Icon", 'label "with" quotes')
        lines = generated_lines(compose, node)
        tree = parse_icon_line(lines[0])
        assert all_call_args_are_string_literals(tree)

    def test_icon_fontname_injection_is_neutralised(self):
        """Injection payload in icon fontname must be escaped."""
        payload = "Arial'); import os; os.system('id')  #"
        compose = make_compose(custom_labels=False)
        node = make_node("VirtualServer Icon", "label", fontname=payload)
        lines = generated_lines(compose, node)
        tree = parse_icon_line(lines[0])
        assert all_call_args_are_string_literals(tree)
        for n in ast.walk(tree):
            assert not isinstance(n, (ast.Import, ast.ImportFrom))
