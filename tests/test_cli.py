"""Tests for the CLI commands (validate and init)."""

from pathlib import Path

from click.testing import CliRunner

from ai_standards.cli import cli


class TestValidateCommand:
    """Tests for the validate CLI command."""

    def test_validate_compliant_repo(self, compliant_repo: Path):
        """Verify a fully compliant repo passes all 11 checks."""
        runner = CliRunner()
        result = runner.invoke(cli, ["validate", str(compliant_repo)])
        assert result.exit_code == 0
        assert "11/11" in result.output

    def test_validate_empty_repo(self, empty_repo: Path):
        """Verify an empty repo only passes naming and docstring checks (2/11)."""
        runner = CliRunner()
        result = runner.invoke(cli, ["validate", str(empty_repo)])
        assert result.exit_code == 1
        # Naming + Docstrings pass (no .py files), rest fail = 2/11
        assert "2/11" in result.output

    def test_validate_partial_repo(self, partial_repo: Path):
        """Verify a partial repo passes README + LICENSE + naming + docstrings (4/11)."""
        runner = CliRunner()
        result = runner.invoke(cli, ["validate", str(partial_repo)])
        assert result.exit_code == 1
        # README + LICENSE + Naming + Docstrings pass = 4/11
        assert "4/11" in result.output

    def test_validate_nonexistent_path(self):
        """Verify validation fails for a nonexistent path."""
        runner = CliRunner()
        result = runner.invoke(cli, ["validate", "/nonexistent/path"])
        assert result.exit_code != 0

    def test_validate_shows_pass_and_fail(self, partial_repo: Path):
        """Verify output contains both PASS and FAIL labels."""
        runner = CliRunner()
        result = runner.invoke(cli, ["validate", str(partial_repo)])
        assert "PASS" in result.output
        assert "FAIL" in result.output


class TestInitCommand:
    """Tests for the init CLI command."""

    def test_init_copies_files(self, empty_repo: Path):
        """Verify init copies baseline config files into an empty repo."""
        runner = CliRunner()
        result = runner.invoke(cli, ["init", str(empty_repo)])
        assert result.exit_code == 0
        assert "COPY" in result.output
        assert (empty_repo / "ruff.toml").exists()
        assert (empty_repo / ".pre-commit-config.yaml").exists()

    def test_init_skips_existing_files(self, tmp_path: Path):
        """Verify init does not overwrite existing config files."""
        # Create existing files
        (tmp_path / "ruff.toml").write_text("# custom config\n")
        (tmp_path / ".pre-commit-config.yaml").write_text("# custom config\n")

        runner = CliRunner()
        result = runner.invoke(cli, ["init", str(tmp_path)])
        assert result.exit_code == 0
        assert "SKIP" in result.output

        # Verify files were not overwritten
        assert (tmp_path / "ruff.toml").read_text() == "# custom config\n"

    def test_init_copies_only_missing(self, tmp_path: Path):
        """Verify init copies only files that do not already exist."""
        # Only ruff.toml exists
        (tmp_path / "ruff.toml").write_text("# existing\n")

        runner = CliRunner()
        result = runner.invoke(cli, ["init", str(tmp_path)])
        assert result.exit_code == 0
        # ruff.toml skipped, pre-commit copied
        assert (tmp_path / ".pre-commit-config.yaml").exists()

    def test_init_nonexistent_path(self):
        """Verify init fails for a nonexistent path."""
        runner = CliRunner()
        result = runner.invoke(cli, ["init", "/nonexistent/path"])
        assert result.exit_code != 0
