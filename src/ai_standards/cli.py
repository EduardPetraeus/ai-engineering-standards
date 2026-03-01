"""CLI for AI Engineering Standards validator."""

from __future__ import annotations

import shutil
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from ai_standards.checks import ALL_CHECKS

console = Console()

# Resolve the package root (repo root) for locating baseline config files.
# src/ai_standards/cli.py -> src/ai_standards -> src -> repo root
PACKAGE_ROOT = Path(__file__).resolve().parent.parent.parent


@click.group()
@click.version_option(package_name="ai-engineering-standards")
def cli() -> None:
    """AI Engineering Standards — validate and bootstrap repos."""


@cli.command()
@click.argument("repo_path", type=click.Path(exists=True, file_okay=False, resolve_path=True))
def validate(repo_path: str) -> None:
    """Validate a repository against engineering standards."""
    path = Path(repo_path)
    console.print(f"\nValidating: [bold]{path}[/bold]\n")

    table = Table(title="Standards Compliance Report")
    table.add_column("Check", style="cyan", no_wrap=True)
    table.add_column("Status", justify="center")
    table.add_column("Details", style="dim")

    passed_count = 0
    total = len(ALL_CHECKS)

    for name, check_fn in ALL_CHECKS:
        passed, detail = check_fn(path)
        if passed:
            passed_count += 1
            status = "[green]PASS[/green]"
        else:
            status = "[red]FAIL[/red]"
        table.add_row(name, status, detail)

    console.print(table)
    console.print(f"\nScore: [bold]{passed_count}/{total}[/bold] checks passed\n")

    # Exit with non-zero if any checks failed
    if passed_count < total:
        raise SystemExit(1)


@cli.command()
@click.argument("repo_path", type=click.Path(exists=True, file_okay=False, resolve_path=True))
def init(repo_path: str) -> None:
    """Copy baseline config files into a target repository."""
    target = Path(repo_path)
    console.print(f"\nInitializing standards in: [bold]{target}[/bold]\n")

    files_to_copy = [
        ("code-style/python/ruff.toml", "ruff.toml"),
        ("code-style/python/.pre-commit-config.yaml", ".pre-commit-config.yaml"),
    ]

    for source_rel, dest_name in files_to_copy:
        source = PACKAGE_ROOT / source_rel
        dest = target / dest_name

        if not source.exists():
            console.print(f"  [yellow]SKIP[/yellow]  {dest_name} — source template not found")
            continue

        if dest.exists():
            console.print(f"  [yellow]SKIP[/yellow]  {dest_name} — already exists")
            continue

        shutil.copy2(source, dest)
        console.print(f"  [green]COPY[/green]  {dest_name}")

    console.print()
