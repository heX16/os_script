# Build and install (release)

This is for the human maintainer when cutting a new release. It is not part of the agent-oriented docs.

## Version sources

The package version is defined in two places:

1. **Canonical runtime version** — `os_script_version()` in [`os_script/os_script.py`](../os_script/os_script.py):

   ```python
   def os_script_version():
       return '0.5.3'
   ```

2. **Packaging metadata** — `version` in [`pyproject.toml`](../pyproject.toml).

When releasing, bump the string returned by `os_script_version()` first. Then run [`build_and_install.py`](../build_and_install.py), which syncs that value into `pyproject.toml` if they differ.

## What `build_and_install.py` does

Run from the repository root:

```bash
python build_and_install.py
```

The script:

1. Reads the version from `os_script_version()` in `os_script/os_script.py`.
2. Updates `pyproject.toml` `version = "..."` if it does not match.
3. Installs the `build` package (`pip install build`).
4. Builds the wheel with `python -m build`.
5. Force-reinstalls the resulting wheel: `dist/os_script-<version>-py3-none-any.whl`.

Note: the script intentionally does not import `os_script` (see the comment at the top of the file).
