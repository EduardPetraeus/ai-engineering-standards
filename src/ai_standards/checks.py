"""Individual standards checks for repository validation."""

from pathlib import Path


def check_ruff_config(repo_path: Path) -> tuple[bool, str]:
    """Check if ruff configuration exists (ruff.toml or [tool.ruff] in pyproject.toml)."""
    ruff_toml = repo_path / "ruff.toml"
    if ruff_toml.exists():
        return True, "ruff.toml found"

    pyproject = repo_path / "pyproject.toml"
    if pyproject.exists():
        content = pyproject.read_text()
        if "[tool.ruff]" in content:
            return True, "[tool.ruff] found in pyproject.toml"

    return False, "No ruff.toml or [tool.ruff] in pyproject.toml"


def check_pyproject(repo_path: Path) -> tuple[bool, str]:
    """Check if pyproject.toml exists with [project] section."""
    pyproject = repo_path / "pyproject.toml"
    if not pyproject.exists():
        return False, "pyproject.toml not found"

    content = pyproject.read_text()
    if "[project]" in content:
        return True, "pyproject.toml with [project] section found"

    return False, "pyproject.toml exists but missing [project] section"


def check_pre_commit(repo_path: Path) -> tuple[bool, str]:
    """Check if .pre-commit-config.yaml exists."""
    pre_commit = repo_path / ".pre-commit-config.yaml"
    if pre_commit.exists():
        return True, ".pre-commit-config.yaml found"
    return False, ".pre-commit-config.yaml not found"


def check_claude_md(repo_path: Path) -> tuple[bool, str]:
    """Check if CLAUDE.md exists."""
    claude_md = repo_path / "CLAUDE.md"
    if claude_md.exists():
        return True, "CLAUDE.md found"
    return False, "CLAUDE.md not found"


def check_tests_dir(repo_path: Path) -> tuple[bool, str]:
    """Check if tests/ directory exists."""
    tests_dir = repo_path / "tests"
    if tests_dir.is_dir():
        return True, "tests/ directory found"
    return False, "tests/ directory not found"


def check_ci_workflows(repo_path: Path) -> tuple[bool, str]:
    """Check if .github/workflows/ directory exists."""
    workflows_dir = repo_path / ".github" / "workflows"
    if workflows_dir.is_dir():
        return True, ".github/workflows/ directory found"
    return False, ".github/workflows/ directory not found"


def check_readme(repo_path: Path) -> tuple[bool, str]:
    """Check if README.md exists."""
    readme = repo_path / "README.md"
    if readme.exists():
        return True, "README.md found"
    return False, "README.md not found"


def check_license(repo_path: Path) -> tuple[bool, str]:
    """Check if LICENSE file exists."""
    license_file = repo_path / "LICENSE"
    if license_file.exists():
        return True, "LICENSE found"
    return False, "LICENSE not found"


ALL_CHECKS: list[tuple[str, callable]] = [
    ("Ruff config", check_ruff_config),
    ("pyproject.toml [project]", check_pyproject),
    ("Pre-commit config", check_pre_commit),
    ("CLAUDE.md", check_claude_md),
    ("Tests directory", check_tests_dir),
    ("CI/CD workflows", check_ci_workflows),
    ("README.md", check_readme),
    ("LICENSE", check_license),
]
