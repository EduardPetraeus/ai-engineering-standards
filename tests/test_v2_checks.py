"""Tests for V2 checks: naming conventions, commit messages, CLAUDE.md sections, docstrings."""

from pathlib import Path

from ai_standards.checks import (
    check_claude_md_sections,
    check_claude_md_sections_repo,
    check_commit_message,
    check_docstrings,
    check_docstrings_repo,
    check_naming_conventions,
    check_naming_conventions_repo,
)

# ---------------------------------------------------------------------------
# Task 1: AST-based Python naming convention check
# ---------------------------------------------------------------------------


class TestNamingConventions:
    """Tests for check_naming_conventions (file-level function)."""

    def test_valid_snake_case_functions(self, tmp_path: Path):
        """Functions with snake_case should produce no violations."""
        py_file = tmp_path / "good.py"
        py_file.write_text("def my_function():\n    pass\n\ndef another_func(arg_one):\n    pass\n")
        violations = check_naming_conventions(py_file)
        assert violations == []

    def test_camel_case_function_detected(self, tmp_path: Path):
        """Functions with camelCase should be flagged."""
        py_file = tmp_path / "bad.py"
        py_file.write_text("def myFunction():\n    pass\n")
        violations = check_naming_conventions(py_file)
        assert len(violations) == 1
        assert violations[0]["kind"] == "function"
        assert violations[0]["name"] == "myFunction"
        assert violations[0]["line"] == 1

    def test_pascal_case_class_valid(self, tmp_path: Path):
        """Classes with PascalCase should produce no violations."""
        py_file = tmp_path / "good_class.py"
        py_file.write_text("class MyClass:\n    pass\n\nclass AnotherOne:\n    pass\n")
        violations = check_naming_conventions(py_file)
        assert violations == []

    def test_snake_case_class_detected(self, tmp_path: Path):
        """Classes with snake_case should be flagged."""
        py_file = tmp_path / "bad_class.py"
        py_file.write_text("class my_class:\n    pass\n")
        violations = check_naming_conventions(py_file)
        assert len(violations) == 1
        assert violations[0]["kind"] == "class"
        assert violations[0]["name"] == "my_class"

    def test_dunder_methods_ignored(self, tmp_path: Path):
        """Dunder methods like __init__ should not be flagged."""
        py_file = tmp_path / "dunder.py"
        py_file.write_text(
            "class MyClass:\n"
            "    def __init__(self):\n"
            "        pass\n"
            "    def __repr__(self):\n"
            "        return ''\n"
        )
        violations = check_naming_conventions(py_file)
        assert violations == []

    def test_upper_case_constants_ignored(self, tmp_path: Path):
        """UPPER_CASE constants should not be flagged as bad variable names."""
        py_file = tmp_path / "constants.py"
        py_file.write_text("MAX_RETRIES = 3\nBASE_URL = 'http://example.com'\n")
        violations = check_naming_conventions(py_file)
        assert violations == []

    def test_mixed_violations(self, tmp_path: Path):
        """A file with multiple violations should report all of them."""
        py_file = tmp_path / "mixed.py"
        py_file.write_text(
            "class bad_class:\n    pass\n\ndef BadFunction():\n    pass\n\nmyVar = 42\n"
        )
        violations = check_naming_conventions(py_file)
        assert len(violations) == 3
        kinds = {v["kind"] for v in violations}
        assert "class" in kinds
        assert "function" in kinds
        assert "variable" in kinds

    def test_syntax_error_file(self, tmp_path: Path):
        """A file with syntax errors should return a syntax_error violation."""
        py_file = tmp_path / "broken.py"
        py_file.write_text("def foo(\n")
        violations = check_naming_conventions(py_file)
        assert len(violations) == 1
        assert violations[0]["kind"] == "syntax_error"

    def test_empty_file(self, tmp_path: Path):
        """An empty Python file should produce no violations."""
        py_file = tmp_path / "empty.py"
        py_file.write_text("")
        violations = check_naming_conventions(py_file)
        assert violations == []

    def test_single_underscore_functions_checked(self, tmp_path: Path):
        """Single-underscore functions are still checked for snake_case."""
        py_file = tmp_path / "private.py"
        py_file.write_text("def _helper():\n    pass\n\ndef _internalSetup():\n    pass\n")
        violations = check_naming_conventions(py_file)
        # _helper is valid snake_case, _internalSetup has uppercase so it is flagged
        assert len(violations) == 1
        assert violations[0]["name"] == "_internalSetup"


class TestNamingConventionsRepo:
    """Tests for check_naming_conventions_repo (repo-level wrapper)."""

    def test_clean_repo_passes(self, tmp_path: Path):
        """A repo with only good naming should pass."""
        py_file = tmp_path / "good.py"
        py_file.write_text("def my_func():\n    pass\n\nclass MyClass:\n    pass\n")
        passed, detail = check_naming_conventions_repo(tmp_path)
        assert passed is True
        assert "All Python names follow conventions" in detail

    def test_bad_repo_fails(self, tmp_path: Path):
        """A repo with naming violations should fail."""
        py_file = tmp_path / "bad.py"
        py_file.write_text("def BadFunction():\n    pass\n")
        passed, detail = check_naming_conventions_repo(tmp_path)
        assert passed is False
        assert "BadFunction" in detail

    def test_venv_ignored(self, tmp_path: Path):
        """Files inside .venv should be ignored."""
        venv_dir = tmp_path / ".venv" / "lib"
        venv_dir.mkdir(parents=True)
        py_file = venv_dir / "badName.py"
        py_file.write_text("def BadFunc():\n    pass\n")
        passed, _ = check_naming_conventions_repo(tmp_path)
        assert passed is True


# ---------------------------------------------------------------------------
# Task 2: Commit message format check
# ---------------------------------------------------------------------------


class TestCommitMessage:
    """Tests for check_commit_message."""

    def test_valid_simple(self):
        """A simple valid conventional commit should pass."""
        valid, errors = check_commit_message("feat: add new feature")
        assert valid is True
        assert errors == []

    def test_valid_with_scope(self):
        """A commit with scope should pass."""
        valid, errors = check_commit_message("fix(auth): resolve login timeout")
        assert valid is True
        assert errors == []

    def test_valid_all_types(self):
        """All valid commit types should pass."""
        types = ["feat", "fix", "docs", "style", "refactor", "test", "chore", "ci", "perf", "build"]
        for commit_type in types:
            valid, errors = check_commit_message(f"{commit_type}: something")
            assert valid is True, f"Type '{commit_type}' should be valid but got errors: {errors}"

    def test_invalid_type(self):
        """An unknown commit type should fail."""
        valid, errors = check_commit_message("feature: add new thing")
        assert valid is False
        assert any("Conventional Commits" in e for e in errors)

    def test_missing_colon(self):
        """A message without colon should fail."""
        valid, errors = check_commit_message("feat add new feature")
        assert valid is False

    def test_too_long_first_line(self):
        """A first line over 72 characters should fail."""
        long_msg = "feat: " + "a" * 70  # 76 chars total
        valid, errors = check_commit_message(long_msg)
        assert valid is False
        assert any("72" in e for e in errors)

    def test_exactly_72_chars(self):
        """A first line of exactly 72 characters should pass."""
        # "feat: " = 6 chars, need 66 more
        msg = "feat: " + "a" * 66
        assert len(msg) == 72
        valid, errors = check_commit_message(msg)
        assert valid is True

    def test_empty_message(self):
        """An empty commit message should fail."""
        valid, errors = check_commit_message("")
        assert valid is False
        assert any("empty" in e.lower() for e in errors)

    def test_multiline_only_first_line_checked(self):
        """Only the first line is checked for format and length."""
        msg = "feat: short summary\n\nThis body can be as long as it wants " + "x" * 200
        valid, errors = check_commit_message(msg)
        assert valid is True

    def test_breaking_change_exclamation(self):
        """Breaking change indicator (!) should be valid."""
        valid, errors = check_commit_message("feat!: breaking change")
        assert valid is True

    def test_whitespace_only(self):
        """A whitespace-only message should fail."""
        valid, errors = check_commit_message("   \n  ")
        assert valid is False


# ---------------------------------------------------------------------------
# Task 3: CLAUDE.md content validation
# ---------------------------------------------------------------------------


class TestClaudeMdSections:
    """Tests for check_claude_md_sections (file-level)."""

    def test_all_sections_present(self, tmp_path: Path):
        """CLAUDE.md with all required sections should pass."""
        claude_md = tmp_path / "CLAUDE.md"
        claude_md.write_text(
            "# CLAUDE.md\n\n"
            "## Identity\nWe are a team.\n\n"
            "## Scope\nThis repo covers X.\n\n"
            "## Boundaries\nDo not do Y.\n"
        )
        valid, missing = check_claude_md_sections(claude_md)
        assert valid is True
        assert missing == []

    def test_missing_one_section(self, tmp_path: Path):
        """CLAUDE.md missing one section should fail with that section listed."""
        claude_md = tmp_path / "CLAUDE.md"
        claude_md.write_text(
            "# CLAUDE.md\n\n## Identity\nWe are a team.\n\n## Scope\nThis repo covers X.\n"
        )
        valid, missing = check_claude_md_sections(claude_md)
        assert valid is False
        assert "Boundaries" in missing

    def test_missing_all_sections(self, tmp_path: Path):
        """CLAUDE.md with no required sections should fail with all listed."""
        claude_md = tmp_path / "CLAUDE.md"
        claude_md.write_text("# CLAUDE.md\n\nJust some text.\n")
        valid, missing = check_claude_md_sections(claude_md)
        assert valid is False
        assert len(missing) == 3

    def test_case_insensitive_headings(self, tmp_path: Path):
        """Section headings should be matched case-insensitively."""
        claude_md = tmp_path / "CLAUDE.md"
        claude_md.write_text(
            "# CLAUDE.md\n\n"
            "## IDENTITY\nWe are a team.\n\n"
            "## scope\nThis repo covers X.\n\n"
            "### Project Boundaries\nDo not do Y.\n"
        )
        valid, missing = check_claude_md_sections(claude_md)
        assert valid is True

    def test_file_not_found(self, tmp_path: Path):
        """A missing CLAUDE.md should fail."""
        claude_md = tmp_path / "CLAUDE.md"
        valid, missing = check_claude_md_sections(claude_md)
        assert valid is False
        assert "CLAUDE.md not found" in missing

    def test_sections_in_different_heading_levels(self, tmp_path: Path):
        """Sections can be at any heading level (h1-h6)."""
        claude_md = tmp_path / "CLAUDE.md"
        claude_md.write_text("# Identity\n\n### Scope\n\n###### Boundaries\n")
        valid, missing = check_claude_md_sections(claude_md)
        assert valid is True


class TestClaudeMdSectionsRepo:
    """Tests for check_claude_md_sections_repo (repo-level wrapper)."""

    def test_compliant_claude_md(self, tmp_path: Path):
        """A repo with a fully compliant CLAUDE.md should pass."""
        claude_md = tmp_path / "CLAUDE.md"
        claude_md.write_text(
            "# CLAUDE.md\n\n## Identity\nBot.\n\n## Scope\nAll.\n\n## Boundaries\nNone.\n"
        )
        passed, detail = check_claude_md_sections_repo(tmp_path)
        assert passed is True

    def test_missing_claude_md(self, tmp_path: Path):
        """A repo without CLAUDE.md should fail."""
        passed, detail = check_claude_md_sections_repo(tmp_path)
        assert passed is False
        assert "not found" in detail

    def test_incomplete_claude_md(self, tmp_path: Path):
        """A repo with an incomplete CLAUDE.md should fail with missing sections."""
        claude_md = tmp_path / "CLAUDE.md"
        claude_md.write_text("# CLAUDE.md\n\n## Identity\nBot.\n")
        passed, detail = check_claude_md_sections_repo(tmp_path)
        assert passed is False
        assert "Scope" in detail
        assert "Boundaries" in detail


# ---------------------------------------------------------------------------
# Task 4: Docstring presence check
# ---------------------------------------------------------------------------


class TestDocstrings:
    """Tests for check_docstrings (file-level)."""

    def test_all_public_functions_documented(self, tmp_path: Path):
        """Public functions with docstrings should produce no violations."""
        py_file = tmp_path / "good.py"
        py_file.write_text(
            "def my_function():\n"
            '    """Does something."""\n'
            "    pass\n\n"
            "def another():\n"
            '    """Another function."""\n'
            "    pass\n"
        )
        violations = check_docstrings(py_file)
        assert violations == []

    def test_missing_docstring_detected(self, tmp_path: Path):
        """A public function without a docstring should be flagged."""
        py_file = tmp_path / "bad.py"
        py_file.write_text("def my_function():\n    pass\n")
        violations = check_docstrings(py_file)
        assert len(violations) == 1
        assert violations[0]["name"] == "my_function"
        assert "missing a docstring" in violations[0]["message"]

    def test_private_functions_ignored(self, tmp_path: Path):
        """Private functions (starting with _) should not be checked."""
        py_file = tmp_path / "private.py"
        py_file.write_text(
            "def _private_helper():\n    pass\n\ndef __double_underscore():\n    pass\n"
        )
        violations = check_docstrings(py_file)
        assert violations == []

    def test_mixed_public_and_private(self, tmp_path: Path):
        """Only public functions without docstrings should be flagged."""
        py_file = tmp_path / "mixed.py"
        py_file.write_text(
            "def public_good():\n"
            '    """Has docstring."""\n'
            "    pass\n\n"
            "def public_bad():\n"
            "    pass\n\n"
            "def _private_no_doc():\n"
            "    pass\n"
        )
        violations = check_docstrings(py_file)
        assert len(violations) == 1
        assert violations[0]["name"] == "public_bad"

    def test_class_methods(self, tmp_path: Path):
        """Public methods in classes should also be checked."""
        py_file = tmp_path / "cls.py"
        py_file.write_text(
            "class MyClass:\n"
            "    def public_method(self):\n"
            '        """Documented."""\n'
            "        pass\n\n"
            "    def undocumented(self):\n"
            "        pass\n"
        )
        violations = check_docstrings(py_file)
        assert len(violations) == 1
        assert violations[0]["name"] == "undocumented"

    def test_empty_file(self, tmp_path: Path):
        """An empty Python file should produce no violations."""
        py_file = tmp_path / "empty.py"
        py_file.write_text("")
        violations = check_docstrings(py_file)
        assert violations == []

    def test_syntax_error_file(self, tmp_path: Path):
        """A file with syntax errors should return a violation."""
        py_file = tmp_path / "broken.py"
        py_file.write_text("def foo(\n")
        violations = check_docstrings(py_file)
        assert len(violations) == 1
        assert "syntax error" in violations[0]["message"].lower()


class TestDocstringsRepo:
    """Tests for check_docstrings_repo (repo-level wrapper)."""

    def test_clean_repo_passes(self, tmp_path: Path):
        """A repo where all public functions have docstrings should pass."""
        py_file = tmp_path / "good.py"
        py_file.write_text('def my_func():\n    """Doc."""\n    pass\n')
        passed, detail = check_docstrings_repo(tmp_path)
        assert passed is True

    def test_bad_repo_fails(self, tmp_path: Path):
        """A repo with missing docstrings should fail."""
        py_file = tmp_path / "bad.py"
        py_file.write_text("def undocumented():\n    pass\n")
        passed, detail = check_docstrings_repo(tmp_path)
        assert passed is False
        assert "undocumented" in detail

    def test_venv_ignored(self, tmp_path: Path):
        """Files inside .venv should be ignored."""
        venv_dir = tmp_path / ".venv" / "lib"
        venv_dir.mkdir(parents=True)
        py_file = venv_dir / "no_docs.py"
        py_file.write_text("def undocumented():\n    pass\n")
        passed, _ = check_docstrings_repo(tmp_path)
        assert passed is True
