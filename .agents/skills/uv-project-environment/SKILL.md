---
name: uv-project-environment
description: Manage StarRailAutomation's Python dependencies, commands, and project-local virtual environment with uv. Use for setup, dependency changes, testing, or application runs in this repository.
---

# UV Project Environment

Use `uv` for every Python environment and dependency operation in this repository. Do not create a virtual environment outside the project or use direct `pip install` for project dependencies.

## Workflow

- Run `uv sync --group dev` from the repository root to create or update the root `.venv` from `pyproject.toml` and `uv.lock`.
- Run application and test commands through `uv run`, for example `uv run star-rail-automation` and `uv run pytest`.
- Add runtime dependencies to `[project.dependencies]`; add test and developer-only dependencies to the `dev` dependency group. Regenerate `uv.lock` with `uv lock` or `uv sync` and commit the lockfile.
- Keep `.venv/` ignored. Do not modify generated files inside it.

Before changing dependencies, inspect `pyproject.toml` and `uv.lock`. If dependency resolution requires network access, request authorization before retrying outside the sandbox.
