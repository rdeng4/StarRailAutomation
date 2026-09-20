# Repository Guidelines

## Project Structure & Module Organization

Application code uses a strict MVP structure under `src/`:

- `presentation/views/` contains PySide6 widgets and layouts only.
- `presentation/presenters/` handles view events and coordinates UI state.
- `presentation/models/` contains pure presentation/domain state types; it must not import PySide6 or run commands.
- `services/` contains pure Python integrations and business operations, such as Waydroid checks; it must not import PySide6.

Views must never call services directly: route work through a presenter and return model data to the view. Keep tests in `tests/` and non-code resources in `assets/` or `tests/fixtures/`. Do not put generated files, local captures, or credentials at the repository root.

## Build, Test, and Development Commands

Use `uv` to manage the root `.venv` and the commands defined in `pyproject.toml`:

- `uv sync --group dev` installs runtime and test dependencies.
- `uv run star-rail-automation` starts the desktop application.
- `uv run pytest` runs the test suite.

## Coding Style & Naming Conventions

Use 4 spaces for Python. Use `snake_case` for modules and functions, `PascalCase` for classes, and descriptive lower-case directory names. Name files by responsibility, for example `waydroid_service.py`. Follow configured formatters and linters rather than hand-formatting against their output.

## Testing Guidelines

Add tests with each behavior change. Mirror source paths under `tests/` where practical and name tests for behavior, such as `test_reports_running_session`. Unit-test models and services without Qt; test presenters with fake views; use PySide6 smoke tests for view layout. Keep game-dependent integration tests isolated and document their local setup. Run the full test suite before opening a pull request.

## Commit & Pull Request Guidelines

The history currently has only an `Initial commit`, so no established commit convention exists. Use concise imperative subjects, optionally scoped: `vision: improve button matching`. Keep commits focused and avoid mixing refactors with behavior changes.

Pull requests should explain the user-visible change, testing performed, and any game/client assumptions. Link related issues when available and include before/after screenshots or recordings for visual-automation changes. Never commit account data, screenshots containing private information, or local configuration secrets.
