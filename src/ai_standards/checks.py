"""Individual standards checks for repository validation."""

import ast
import re
from pathlib import Path

# --- Regex patterns ---

_SNAKE_CASE_RE = re.compile(r"^_*[a-z][a-z0-9]*(_[a-z0-9]+)*_?$")
_PASCAL_CASE_RE = re.compile(r"^_*[A-Z][a-zA-Z0-9]*$")
_CONVENTIONAL_COMMIT_RE = re.compile(
    r"^(feat|fix|docs|style|refactor|test|chore|ci|perf|build)"
    r"(\([a-zA-Z0-9_\-./]+\))?!?: .+"
)

_CLAUDE_MD_REQUIRED_SECTIONS = ["Identity", "Scope", "Boundaries"]

# ---------------------------------------------------------------------------
# Existing file-existence checks
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# NEW: AST-based Python naming convention check (Task 1)
# ---------------------------------------------------------------------------


def _is_snake_case(name: str) -> bool:
    """Return True if *name* follows snake_case convention."""
    return bool(_SNAKE_CASE_RE.match(name))


def _is_pascal_case(name: str) -> bool:
    """Return True if *name* follows PascalCase convention."""
    return bool(_PASCAL_CASE_RE.match(name))


def check_naming_conventions(file_path: Path) -> list[dict[str, str | int]]:
    """Parse a Python file with AST and return naming-convention violations.

    Returns a list of dicts with keys: file, line, name, kind, message.
    """
    source = file_path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(source, filename=str(file_path))
    except SyntaxError:
        return [
            {
                "file": str(file_path),
                "line": 0,
                "name": "",
                "kind": "syntax_error",
                "message": "Could not parse file (syntax error)",
            }
        ]

    violations: list[dict[str, str | int]] = []
    file_str = str(file_path)

    for node in ast.walk(tree):
        # Class names must be PascalCase
        if isinstance(node, ast.ClassDef):
            if not _is_pascal_case(node.name):
                violations.append(
                    {
                        "file": file_str,
                        "line": node.lineno,
                        "name": node.name,
                        "kind": "class",
                        "message": f"Class '{node.name}' should be PascalCase",
                    }
                )

        # Function / method names must be snake_case
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Allow dunder methods and test doubles
            if not node.name.startswith("__") and not _is_snake_case(node.name):
                violations.append(
                    {
                        "file": file_str,
                        "line": node.lineno,
                        "name": node.name,
                        "kind": "function",
                        "message": f"Function '{node.name}' should be snake_case",
                    }
                )

        # Top-level variable assignments (simple Name targets only)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    name = target.id
                    # Skip UPPER_CASE constants and private names
                    if name.isupper() or name.startswith("_"):
                        continue
                    if not _is_snake_case(name):
                        violations.append(
                            {
                                "file": file_str,
                                "line": node.lineno,
                                "name": name,
                                "kind": "variable",
                                "message": f"Variable '{name}' should be snake_case",
                            }
                        )

    return violations


def check_naming_conventions_repo(repo_path: Path) -> tuple[bool, str]:
    """Run naming convention checks on all .py files in repo_path.

    Returns (passed, detail) tuple compatible with ALL_CHECKS.
    """
    all_violations: list[dict[str, str | int]] = []
    py_files = list(repo_path.rglob("*.py"))

    # Skip common non-source directories
    skip_dirs = {".venv", "venv", "node_modules", ".git", "__pycache__", ".tox", ".eggs"}

    for py_file in py_files:
        if any(part in skip_dirs for part in py_file.parts):
            continue
        all_violations.extend(check_naming_conventions(py_file))

    if not all_violations:
        return True, "All Python names follow conventions"

    summary_lines = [f"{v['file']}:{v['line']}: {v['message']}" for v in all_violations[:5]]
    extra = len(all_violations) - 5
    detail = "; ".join(summary_lines)
    if extra > 0:
        detail += f" (+{extra} more)"
    return False, detail


# ---------------------------------------------------------------------------
# NEW: Commit message format check (Task 2)
# ---------------------------------------------------------------------------


def check_commit_message(message: str) -> tuple[bool, list[str]]:
    """Validate a commit message against Conventional Commits.

    Returns (valid, list_of_errors).
    """
    errors: list[str] = []
    if not message or not message.strip():
        return False, ["Commit message is empty"]

    first_line = message.strip().splitlines()[0]

    if len(first_line) > 72:
        errors.append(f"First line is {len(first_line)} chars (max 72)")

    if not _CONVENTIONAL_COMMIT_RE.match(first_line):
        errors.append(
            "First line does not match Conventional Commits: "
            "type(scope): description or type: description"
        )

    return (len(errors) == 0), errors


# ---------------------------------------------------------------------------
# NEW: CLAUDE.md content validation (Task 3)
# ---------------------------------------------------------------------------


def check_claude_md_sections(file_path: Path) -> tuple[bool, list[str]]:
    """Check that CLAUDE.md contains required sections: Identity, Scope, Boundaries.

    Looks for markdown headings (any level) containing the section name.
    Returns (valid, list_of_missing_sections).
    """
    if not file_path.exists():
        return False, ["CLAUDE.md not found"]

    content = file_path.read_text(encoding="utf-8")
    # Match headings like ## Identity, # Scope, ### Boundaries (case-insensitive)
    heading_pattern = re.compile(r"^#{1,6}\s+(.+)$", re.MULTILINE)
    headings = [m.group(1).strip().lower() for m in heading_pattern.finditer(content)]

    missing = []
    for section in _CLAUDE_MD_REQUIRED_SECTIONS:
        if not any(section.lower() in h for h in headings):
            missing.append(section)

    if missing:
        return False, missing
    return True, []


def check_claude_md_sections_repo(repo_path: Path) -> tuple[bool, str]:
    """Run CLAUDE.md section validation on a repo.

    Returns (passed, detail) tuple compatible with ALL_CHECKS.
    """
    claude_md = repo_path / "CLAUDE.md"
    if not claude_md.exists():
        return False, "CLAUDE.md not found"

    valid, missing = check_claude_md_sections(claude_md)
    if valid:
        return True, "CLAUDE.md contains all required sections (Identity, Scope, Boundaries)"

    return False, f"CLAUDE.md missing sections: {', '.join(missing)}"


# ---------------------------------------------------------------------------
# NEW: Docstring presence check (Task 4)
# ---------------------------------------------------------------------------


def check_docstrings(file_path: Path) -> list[dict[str, str | int]]:
    """Check that all public functions/methods have docstrings.

    Public = name does not start with underscore.
    Returns list of dicts with keys: file, line, name, message.
    """
    source = file_path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(source, filename=str(file_path))
    except SyntaxError:
        return [
            {
                "file": str(file_path),
                "line": 0,
                "name": "",
                "message": "Could not parse file (syntax error)",
            }
        ]

    violations: list[dict[str, str | int]] = []
    file_str = str(file_path)

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Skip private/protected functions
            if node.name.startswith("_"):
                continue

            docstring = ast.get_docstring(node)
            if not docstring:
                violations.append(
                    {
                        "file": file_str,
                        "line": node.lineno,
                        "name": node.name,
                        "message": f"Public function '{node.name}' is missing a docstring",
                    }
                )

    return violations


def check_docstrings_repo(repo_path: Path) -> tuple[bool, str]:
    """Run docstring presence checks on all .py files in repo_path.

    Returns (passed, detail) tuple compatible with ALL_CHECKS.
    """
    all_violations: list[dict[str, str | int]] = []
    py_files = list(repo_path.rglob("*.py"))

    skip_dirs = {".venv", "venv", "node_modules", ".git", "__pycache__", ".tox", ".eggs"}

    for py_file in py_files:
        if any(part in skip_dirs for part in py_file.parts):
            continue
        all_violations.extend(check_docstrings(py_file))

    if not all_violations:
        return True, "All public functions have docstrings"

    summary_lines = [f"{v['file']}:{v['line']}: {v['message']}" for v in all_violations[:5]]
    extra = len(all_violations) - 5
    detail = "; ".join(summary_lines)
    if extra > 0:
        detail += f" (+{extra} more)"
    return False, detail


# ---------------------------------------------------------------------------
# Check registry
# ---------------------------------------------------------------------------

ALL_CHECKS: list[tuple[str, callable]] = [
    ("Ruff config", check_ruff_config),
    ("pyproject.toml [project]", check_pyproject),
    ("Pre-commit config", check_pre_commit),
    ("CLAUDE.md", check_claude_md),
    ("CLAUDE.md sections", check_claude_md_sections_repo),
    ("Tests directory", check_tests_dir),
    ("CI/CD workflows", check_ci_workflows),
    ("README.md", check_readme),
    ("LICENSE", check_license),
    ("Naming conventions", check_naming_conventions_repo),
    ("Docstring presence", check_docstrings_repo),
]
