# AGENTS.md

Brief guide for AI agents working in this repository.

## Project brief

`os_script` is a Python utility library for OS/shell scripting. It provides helpers for:

- running shell commands (`run_command`, `sh`)
- file and directory operations (copy, remove, find, timestamps)
- process listing/inspection (via `psutil`)
- datetime parsing/formatting and small text/config utilities

## Documentation map

There is no separate Sphinx/MkDocs site. Prefer these sources:

- [`README.md`](README.md) — one-line project overview.
- [`docs/important_functions.md`](docs/important_functions.md) — grouped index of commonly used functions (names only).
- [`os_script/os_script.py`](os_script/os_script.py) — code base, **primary source of truth**: docstrings and section headers (`# Files`, `# Run`, `# Proc`, `# Date time`, etc.).
- [`tests/tests_files.py`](tests/tests_files.py) and [`tests/tests_datetime.py`](tests/tests_datetime.py) — executable specification of expected behavior.
- [`examples/`](examples) — usage snippets (`examples.py`, `test.py`).

Secondary / incomplete modules:

- [`os_script/os_script.systemd.py`](os_script/os_script.systemd.py) — systemd unit helpers (Linux-oriented).
- [`os_script/os_script.storage.py`](os_script/os_script.storage.py) — currently empty placeholder.
- etc.

## Tests

```bash
python run_tests.py
```

This discovers `tests/tests_*.py` via unittest (see [`run_tests.py`](run_tests.py)).

## Conventions

- Write code comments in English.
- Prefer single quotes for Python strings (`'`).
