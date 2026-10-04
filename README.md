# os_script

Library for operation system scripting in Python.

- Run shell commands via `run_command()` or multi-line `sh()` (optionally capture output).
- File helpers: find/list, read/write content, copy/move/remove, timestamps.
- Process helpers (via `psutil`).
- Datetime formatting/parsing and small config/text utilities.

## Install

PyPI: [https://pypi.org/project/os-script/](https://pypi.org/project/os-script/)

```bash
pip install os-script
```

## Quick example

```python
from os_script import find, run_command, sh

result = run_command('python --version', capture_output=True)
print(result.stdout.getvalue().strip())

for path in find('.', '*.py', recursively=True):
    print(path)

sh('echo hello\necho world')
```
