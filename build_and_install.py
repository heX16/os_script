# Release script that does not import os_script, so a broken library can still be packaged.

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

parser = argparse.ArgumentParser(
    description='Build and install os_script. Pass --public to upload to PyPI.'
)
parser.add_argument(
    '--public',
    action='store_true',
    help='Upload the built distributions for this version to PyPI',
)
args = parser.parse_args()


def run_checked(command: list[str]) -> None:
    """A failed build or upload must stop the release."""
    result = subprocess.run(command)
    if result.returncode != 0:
        print(f'Command failed ({result.returncode}): {command}')
        exit(result.returncode)


# Commands below use paths relative to the repository, not to the caller's working directory.
repo_root = Path(__file__).resolve().parent
os.chdir(repo_root)

# The version users see is os_script_version(). pyproject.toml must carry the same value, because pip and PyPI read it from there.
file_path = Path('os_script/os_script.py')
lines = file_path.read_text().splitlines()

try:
    index = lines.index('def os_script_version():')
    version_line = lines[index + 1]
    match = re.search(r"return\s+'([\d.]+)'", version_line)
    if match:
        version = match.group(1)
        print('Version "os_script":', version)
    else:
        print('No version found')
        exit(1)

except ValueError:
    print('The target line was not found in the file.')
    exit(1)
except Exception as e:
    print(f'Error: {e}')
    exit(1)

# Write that version into pyproject.toml only when it differs, so a rerun does not touch the file for no reason.
pyproject_path = Path('pyproject.toml')
pyproject_text = pyproject_path.read_text()

version_pattern = re.compile(r'version\s*=\s*"([\d.]+)"')
current_version_match = version_pattern.search(pyproject_text)
if current_version_match:
    current_version = current_version_match.group(1)
    if version != current_version:
        updated_pyproject_text = version_pattern.sub(f'version = "{version}"', pyproject_text)
        pyproject_path.write_text(updated_pyproject_text)
        print(f'Updated pyproject.toml from {current_version} to {version} version.')
    else:
        print(f'No update needed. Current version is already: {current_version}')
else:
    print('Version line not found in pyproject.toml')
    exit(1)

# Build with the interpreter that runs this script. `pip` and `python` on PATH may be a different installation.
py = sys.executable
run_checked([py, '-m', 'pip', 'install', 'build'])
run_checked([py, '-m', 'build'])

# This version only. A bare prefix such as `0.5.8*` would also match `0.5.80`.
# The sdist is `name-version.tar.gz`; wheels are `name-version-...whl`.
dist_dir = Path('dist')
prefix = f'os_script-{version}'
artifacts = sorted(dist_dir.glob(f'{prefix}*'), key=lambda path: path.name.lower())
artifacts = [
    path for path in artifacts
    if path.name == f'{prefix}.tar.gz' or path.name.startswith(prefix + '-')
]
wheel_files = [path for path in artifacts if path.suffix == '.whl']

# Install the wheel just built, replacing any older copy already present in this environment.
if wheel_files:
    wheel_file = wheel_files[0]
    print(f'Installing version: {wheel_file}')
    run_checked([py, '-m', 'pip', 'install', str(wheel_file), '--force-reinstall'])
else:
    print(f'Wheel file matching os_script-{version}-*.whl not found in {dist_dir}')
    exit(1)

# Upload those same files only when asked. PyPI keeps every uploaded version, so older files in dist/ must not be sent again.
if args.public:
    if not artifacts:
        print(f'No distribution files for version {version} in {dist_dir}')
        exit(1)
    print('Uploading to PyPI:', ', '.join(str(path) for path in artifacts))
    run_checked([py, '-m', 'pip', 'install', 'twine'])
    run_checked([py, '-m', 'twine', 'upload', *[str(path) for path in artifacts]])
