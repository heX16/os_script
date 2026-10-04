# Example: rewrite of build_and_install.py using os_script library helpers.
# Original script at repo root is left unchanged.

import re
import sys
from pathlib import Path

# Bootstrap local package import when running from examples/
repo_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root))

from os_script import *


def run_checked(command: str) -> None:
    """Run a shell command and exit on non-zero return code."""
    result = run_command(command, capture_output=True)
    if result.returncode != 0:
        stderr = result.stderr.read() if result.stderr else ''
        stdout = result.stdout.read() if result.stdout else ''
        print(f'Command failed ({result.returncode}): {command}')
        if stdout:
            print(stdout)
        if stderr:
            print(stderr)
        exit(result.returncode)


# Ensure relative paths resolve from the repository root
cd(repo_root)

# Version from the library itself (instead of parsing source with regex)
version = os_script_version()
print('Version "os_script":', version)

# Sync version into pyproject.toml
pyproject_path = Path('pyproject.toml')
pyproject_text = get_file_content(pyproject_path)

version_pattern = re.compile(r'version\s*=\s*"([\d.]+)"')
current_version_match = version_pattern.search(pyproject_text)
if current_version_match:
    current_version = current_version_match.group(1)
    if version != current_version:
        updated_pyproject_text = version_pattern.sub(f'version = "{version}"', pyproject_text)
        save_file_content(pyproject_path, updated_pyproject_text)
        print(f'Updated pyproject.toml from {current_version} to {version} version.')
    else:
        print(f'No update needed. Current version is already: {current_version}')
else:
    print('Version line not found in pyproject.toml')
    exit(1)

# Build the project
run_checked(f'"{sys.executable}" -m pip install build')
run_checked(f'"{sys.executable}" -m build')

# Find wheel by mask (more robust than a fixed filename)
dist_dir = Path('dist')
wheel_files = list(find(dist_dir, f'os_script-{version}-*.whl'))
wheel_files = file_list_sort_by_name(wheel_files)

if wheel_files:
    wheel_file = wheel_files[0]
    print(f'Installing version: {wheel_file}')
    run_checked(f'"{sys.executable}" -m pip install "{wheel_file}" --force-reinstall')
else:
    print(f'Wheel file matching os_script-{version}-*.whl not found in {dist_dir}')
    exit(1)
