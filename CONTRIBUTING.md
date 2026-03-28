# Contributing to psoul

Thanks for your interest in contributing! psoul is in early development
(v0.0.x) and is founder-directed while the architecture settles. Bug
reports and small fixes are welcome; please open an issue before starting
work on larger changes so we can discuss the approach.

## Setup

1. Install [uv](https://docs.astral.sh/uv/) and
   [just](https://just.systems/).
2. Clone the repo and run the checks:

   ```bash
   git clone https://github.com/oxenfree999/psoul.git
   cd psoul
   just
   ```

## Development workflow

The [justfile](justfile) has the common commands. `just` is optional —
the underlying `uv run` commands work fine on their own.

| Command       | What it does                           |
|---------------|----------------------------------------|
| `just`        | Format, lint, type-check, and test     |
| `just format` | Auto-fix formatting and lint issues    |
| `just lint`   | Lint, format check, and type-check     |
| `just test`   | Run the test suite                     |
| `just snap`   | Update inline snapshot tests           |

## Pull requests

- Work against `main`.
- Include tests for new functionality and bug fixes.
- Run `just` before pushing — CI will run the same checks.
- Keep commits focused. Use
  [conventional commit](https://www.conventionalcommits.org/) prefixes
  (`feat:`, `fix:`, `test:`, `docs:`, etc.).

## Code style

- Ruff handles linting and formatting (`ALL` rules enabled).
- Type checking via [ty](https://github.com/astral-sh/ty).
- Line length: 120 characters.
- Tests live in `tests/` and use pytest with strict mode.

## Reporting bugs

Open an issue with:

- What you expected to happen.
- What actually happened.
- Steps to reproduce (minimal example preferred).
- Python version and OS.
