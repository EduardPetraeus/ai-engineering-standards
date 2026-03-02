"""Shared fixtures for standards validator tests."""

from pathlib import Path

import pytest


@pytest.fixture
def empty_repo(tmp_path: Path) -> Path:
    """Create a bare-minimum empty directory simulating a repo with no standards."""
    return tmp_path


@pytest.fixture
def compliant_repo(tmp_path: Path) -> Path:
    """Create a fully compliant repository with all required files."""
    # ruff.toml
    (tmp_path / "ruff.toml").write_text("[lint]\nselect = ['E', 'F']\n")

    # pyproject.toml with [project] section
    (tmp_path / "pyproject.toml").write_text("[project]\nname = 'test-repo'\nversion = '0.1.0'\n")

    # .pre-commit-config.yaml
    (tmp_path / ".pre-commit-config.yaml").write_text("repos: []\n")

    # CLAUDE.md with required sections
    (tmp_path / "CLAUDE.md").write_text(
        "# CLAUDE.md\n\n"
        "## Identity\nTest project.\n\n"
        "## Scope\nEverything.\n\n"
        "## Boundaries\nNothing out of scope.\n"
    )

    # tests/ directory
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "__init__.py").write_text("")

    # .github/workflows/
    (tmp_path / ".github" / "workflows").mkdir(parents=True)
    (tmp_path / ".github" / "workflows" / "ci.yml").write_text("name: CI\n")

    # README.md
    (tmp_path / "README.md").write_text("# Test Repo\n")

    # LICENSE
    (tmp_path / "LICENSE").write_text("MIT License\n")

    return tmp_path


@pytest.fixture
def partial_repo(tmp_path: Path) -> Path:
    """Create a partially compliant repository (only README and LICENSE)."""
    (tmp_path / "README.md").write_text("# Partial Repo\n")
    (tmp_path / "LICENSE").write_text("MIT License\n")
    return tmp_path


@pytest.fixture
def ruff_in_pyproject_repo(tmp_path: Path) -> Path:
    """Create a repo with ruff config inside pyproject.toml instead of ruff.toml."""
    (tmp_path / "pyproject.toml").write_text(
        "[project]\nname = 'test'\nversion = '0.1.0'\n\n[tool.ruff]\nline-length = 100\n"
    )
    return tmp_path
