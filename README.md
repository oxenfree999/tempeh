# psoul

A CLI and TUI Python session supervisor with batteries included.

> **v0.0.x — early development.** psoul is public from the first commit
> but the API, CLI surface, and event schema are unstable. Breaking changes
> may land in any release until v0.1.0.

## Install

```bash
uv add psoul
```

Or try it without installing:

```bash
uvx psoul --help
```

## Quick start

```bash
psoul version        # print installed version
psoul doctor         # check your Python environment
```

## Development

psoul uses [uv](https://docs.astral.sh/uv/) for package management.
[just](https://just.systems/) provides shorthand dev commands but is
optional — the underlying `uv run` commands work fine on their own.

```bash
uv sync --group dev --group test
just          # run lint fixes + tests
just test     # run tests only
just lint     # check lint + formatting (CI-style)
just fix      # auto-fix lint + format
just snap     # update inline snapshots
just check    # lint + test without modifying files
```

CI runs on Ubuntu, macOS, and Windows across Python 3.12, 3.13, and 3.14.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)
