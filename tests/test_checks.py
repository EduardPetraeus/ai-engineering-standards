"""Tests for individual standards check functions."""

from pathlib import Path

from ai_standards.checks import (
    check_ci_workflows,
    check_claude_md,
    check_license,
    check_pre_commit,
    check_pyproject,
    check_readme,
    check_ruff_config,
    check_tests_dir,
)


class TestCheckRuffConfig:
    def test_pass_with_ruff_toml(self, compliant_repo: Path):
        passed, detail = check_ruff_config(compliant_repo)
        assert passed is True
        assert "ruff.toml" in detail

    def test_pass_with_tool_ruff_in_pyproject(self, ruff_in_pyproject_repo: Path):
        passed, detail = check_ruff_config(ruff_in_pyproject_repo)
        assert passed is True
        assert "[tool.ruff]" in detail

    def test_fail_when_missing(self, empty_repo: Path):
        passed, detail = check_ruff_config(empty_repo)
        assert passed is False

    def test_fail_pyproject_without_ruff(self, tmp_path: Path):
        (tmp_path / "pyproject.toml").write_text("[project]\nname = 'x'\n")
        passed, _ = check_ruff_config(tmp_path)
        assert passed is False


class TestCheckPyproject:
    def test_pass_with_project_section(self, compliant_repo: Path):
        passed, detail = check_pyproject_toml(compliant_repo)
        assert passed is True
        assert "[project]" in detail

    def test_fail_when_missing(self, empty_repo: Path):
        passed, _ = check_pyproject_toml(empty_repo)
        assert passed is False

    def test_fail_without_project_section(self, tmp_path: Path):
        (tmp_path / "pyproject.toml").write_text("[tool.ruff]\nline-length = 100\n")
        passed, detail = check_pyproject_toml(tmp_path)
        assert passed is False
        assert "missing [project]" in detail


class TestCheckPreCommit:
    def test_pass(self, compliant_repo: Path):
        passed, _ = check_pre_commit(compliant_repo)
        assert passed is True

    def test_fail(self, empty_repo: Path):
        passed, _ = check_pre_commit(empty_repo)
        assert passed is False


class TestCheckClaudeMd:
    def test_pass(self, compliant_repo: Path):
        passed, _ = check_claude_md(compliant_repo)
        assert passed is True

    def test_fail(self, empty_repo: Path):
        passed, _ = check_claude_md(empty_repo)
        assert passed is False


class TestCheckTestsDir:
    def test_pass(self, compliant_repo: Path):
        passed, _ = check_tests_dir(compliant_repo)
        assert passed is True

    def test_fail(self, empty_repo: Path):
        passed, _ = check_tests_dir(empty_repo)
        assert passed is False


class TestCheckCiWorkflows:
    def test_pass(self, compliant_repo: Path):
        passed, _ = check_ci_workflows(compliant_repo)
        assert passed is True

    def test_fail(self, empty_repo: Path):
        passed, _ = check_ci_workflows(empty_repo)
        assert passed is False


class TestCheckReadme:
    def test_pass(self, compliant_repo: Path):
        passed, _ = check_readme(compliant_repo)
        assert passed is True

    def test_fail(self, empty_repo: Path):
        passed, _ = check_readme(empty_repo)
        assert passed is False


class TestCheckLicense:
    def test_pass(self, compliant_repo: Path):
        passed, _ = check_license(compliant_repo)
        assert passed is True

    def test_fail(self, empty_repo: Path):
        passed, _ = check_license(empty_repo)
        assert passed is False


# Use the correct function name alias for readability
check_pyproject_toml = check_pyproject
