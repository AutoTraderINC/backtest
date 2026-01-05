# Coding Standards & Linting Guide

To maintain a high-quality, consistent codebase, this project uses **Ruff** for linting and formatting. Ruff is an extremely fast Python linter and formatter that replaces tools like Black, Flake8, and isort.

---

## Quick Start (Command Line)

If you have `uv` installed, you can run the following commands from the project root:

### 1. Check for Issues
This scans the code for bugs, unused imports, and style violations.
```bash
uv run ruff check .
```

### 2. Auto-Fix Common Issues
Ruff can automatically fix many common linting errors (like unused imports).
```bash
uv run ruff check . --fix
```

### 3. Format the Whole Project
This standardizes spacing, quotes, and line breaks across all files.
```bash
uv run ruff format .
```

## Rules & Configuration

Our project rules are defined in the `[tool.ruff]` section of [pyproject.toml](pyproject.toml).

*   **Style**: We follow the "Black" style (4 spaces, double quotes).
*   **Line Length**: Maximum **88 characters**.
*   **Imports**: Automatically sorted and grouped.
*   **Best Practices**: We enforce rules from `pyflakes`, `pycodestyle`, `flake8-bugbear`, and `mccabe`.

---

## Pre-Commit Hook (Optional)
If you'd like to ensure you never commit unformatted code, you can add a script to your local git hooks or just get into the habit of running `uv run ruff check . --fix && uv run ruff format .` before every push.
