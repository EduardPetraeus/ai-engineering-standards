# CLAUDE.md — ai-engineering-standards

This file governs all AI agent sessions in this repository.

## Identity

AI engineering standards validator and linter for agentic development workflows.
Part of the Agentic Engineering OS — provides the "how to do it" layer
(conventions, testing, git, security) that complements the governance framework.

## Scope

- Machine-readable coding conventions: naming, docstrings, commit messages, CLAUDE.md sections
- AST-based Python validators (`ai-standards validate`)
- Scaffold command to initialize new repos with baseline configs (`ai-standards init`)
- Reference config files: ruff.toml, .pre-commit-config.yaml
- This repo validates itself via CI (self-validate job)

## Boundaries

- Do NOT implement governance policy logic — that belongs in `ai-governance-framework`
- Do NOT implement task/project management — that belongs in `ai-project-management`
- Do NOT modify or generate application code — only validate and lint it
- Do NOT store secrets, credentials, or real project data
- Checks are read-only: they report violations but never auto-fix source code

## project_context

- Repo: ai-engineering-standards
- Purpose: Machine-readable coding conventions for agentic development
- License: MIT
- Status: v2.0.0

## conventions

- All content in English
- File names: kebab-case.md for docs, snake_case.py for Python
- Configs use standard tool formats (ruff.toml, pyproject.toml)
- Every standard must include examples
- snake_case for variables/functions, PascalCase for classes, UPPER_SNAKE_CASE for constants

## session_protocol

1. Read this CLAUDE.md
2. Confirm scope
3. After changes: verify examples are correct and copy-pasteable
4. Verify cross-references resolve
5. Run `python -m pytest tests/ -v` before claiming done

## framework_references

- Governance: ~/Github repos/ai-governance-framework
- Project Management: ~/Github repos/ai-project-management
- Umbrella: ~/Github repos/agentic-engineering
