# Run all fixes and tests
all: fix test

# Run the test suite
test *args:
    uv run pytest {{ args }}

# Run linter and formatter checks (read-only, CI-style)
lint:
    uv run ruff check .
    uv run ruff format --check .

# Auto-fix lint issues and format code
fix:
    uv run ruff format .
    uv run ruff check --fix .

# Format code
fmt:
    uv run ruff format .

# Update snapshot tests
snap:
    uv run pytest tests/test_cli_snapshots.py --inline-snapshot=update

# Run all checks without modifying files (CI-style)
check: lint test
