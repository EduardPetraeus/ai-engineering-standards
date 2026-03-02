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
    """Tests for the ruff config file detection check."""

    def test_pass_with_ruff_toml(self, compliant_repo: Path):
        """Verify ruff.toml is detected in a compliant repo."""
        passed, detail = check_ruff_config(compliant_repo)
        assert passed is True
        assert "ruff.toml" in detail

    def test_pass_with_tool_ruff_in_pyproject(self, ruff_in_pyproject_repo: Path):
        """Verify [tool.ruff] in pyproject.toml is detected as valid config."""
        passed, detail = check_ruff_config(ruff_in_pyproject_repo)
        assert passed is True
        assert "[tool.ruff]" in detail

    def test_fail_when_missing(self, empty_repo: Path):
        """Verify check fails when no ruff config exists."""
        passed, detail = check_ruff_config(empty_repo)
        assert passed is False

    def test_fail_pyproject_without_ruff(self, tmp_path: Path):
        """Verify pyproject.toml without [tool.ruff] does not satisfy the check."""
        (tmp_path / "pyproject.toml").write_text("[project]\nname = 'x'\n")
        passed, _ = check_ruff_config(tmp_path)
        assert passed is False


class TestCheckPyproject:
    """Tests for the pyproject.toml [project] section check."""

    def test_pass_with_project_section(self, compliant_repo: Path):
        """Verify pyproject.toml with [project] section passes."""
        passed, detail = check_pyproject_toml(compliant_repo)
        assert passed is True
        assert "[project]" in detail

    def test_fail_when_missing(self, empty_repo: Path):
        """Verify check fails when pyproject.toml does not exist."""
        passed, _ = check_pyproject_toml(empty_repo)
        assert passed is False

    def test_fail_without_project_section(self, tmp_path: Path):
        """Verify pyproject.toml without [project] section fails."""
        (tmp_path / "pyproject.toml").write_text("[tool.ruff]\nline-length = 100\n")
        passed, detail = check_pyproject_toml(tmp_path)
        assert passed is False
        assert "missing [project]" in detail


class TestCheckPreCommit:
    """Tests for the pre-commit config existence check."""

    def test_pass(self, compliant_repo: Path):
        """Verify check passes when .pre-commit-config.yaml exists."""
        passed, _ = check_pre_commit(compliant_repo)
        assert passed is True

    def test_fail(self, empty_repo: Path):
        """Verify check fails when .pre-commit-config.yaml is missing."""
        passed, _ = check_pre_commit(empty_repo)
        assert passed is False


class TestCheckClaudeMd:
    """Tests for the CLAUDE.md existence check."""

    def test_pass(self, compliant_repo: Path):
        """Verify check passes when CLAUDE.md exists."""
        passed, _ = check_claude_md(compliant_repo)
        assert passed is True

    def test_fail(self, empty_repo: Path):
        """Verify check fails when CLAUDE.md is missing."""
        passed, _ = check_claude_md(empty_repo)
        assert passed is False


class TestCheckTestsDir:
    """Tests for the tests/ directory existence check."""

    def test_pass(self, compliant_repo: Path):
        """Verify check passes when tests/ directory exists."""
        passed, _ = check_tests_dir(compliant_repo)
        assert passed is True

    def test_fail(self, empty_repo: Path):
        """Verify check fails when tests/ directory is missing."""
        passed, _ = check_tests_dir(empty_repo)
        assert passed is False


class TestCheckCiWorkflows:
    """Tests for the CI workflows directory existence check."""

    def test_pass(self, compliant_repo: Path):
        """Verify check passes when .github/workflows/ exists."""
        passed, _ = check_ci_workflows(compliant_repo)
        assert passed is True

    def test_fail(self, empty_repo: Path):
        """Verify check fails when .github/workflows/ is missing."""
        passed, _ = check_ci_workflows(empty_repo)
        assert passed is False


class TestCheckReadme:
    """Tests for the README.md existence check."""

    def test_pass(self, compliant_repo: Path):
        """Verify check passes when README.md exists."""
        passed, _ = check_readme(compliant_repo)
        assert passed is True

    def test_fail(self, empty_repo: Path):
        """Verify check fails when README.md is missing."""
        passed, _ = check_readme(empty_repo)
        assert passed is False


class TestCheckLicense:
    """Tests for the LICENSE file existence check."""

    def test_pass(self, compliant_repo: Path):
        """Verify check passes when LICENSE file exists."""
        passed, _ = check_license(compliant_repo)
        assert passed is True

    def test_fail(self, empty_repo: Path):
        """Verify check fails when LICENSE file is missing."""
        passed, _ = check_license(empty_repo)
        assert passed is False


# Use the correct function name alias for readability
check_pyproject_toml = check_pyproject
