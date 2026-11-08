# Same release steps as build_and_install.py, written with os_script helpers.
# Always load the package that sits next to this script, never an installed copy.

import argparse
import importlib.util
import re
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


def load_local_os_script(repo_root: Path) -> None:
    """Load the os_script package that sits next to this script."""
    package_dir = repo_root / 'os_script'
    package_init = package_dir / '__init__.py'
    if not package_init.is_file():
        print(f'Local os_script package not found: {package_init}')
        exit(1)

    # An installed copy may already be in memory. Drop it so the inner import uses this folder.
    for name in list(sys.modules):
        if name == 'os_script' or name.startswith('os_script.'):
            del sys.modules[name]

    spec = importlib.util.spec_from_file_location(
        'os_script',
        package_init,
        submodule_search_locations=[str(package_dir)],
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules['os_script'] = module
    spec.loader.exec_module(module)


repo_root = Path(__file__).resolve().parent
load_local_os_script(repo_root)
from os_script import *


def run_checked(command: str) -> None:
    """A failed build or upload must stop the release."""
    result = run_command(command)
    if result.returncode != 0:
        print(f'Command failed ({result.returncode}): {command}')
        exit(result.returncode)


# Commands below use paths relative to the repository, not to the caller's working directory.
cd(repo_root)

# The version users see is os_script_version(). pyproject.toml must carry the same value, because pip and PyPI read it from there.
version = os_script_version()
print('Version "os_script":', version)

# Write that version into pyproject.toml only when it differs, so a rerun does not touch the file for no reason.
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

# Build with the interpreter that runs this script. `pip` and `python` on PATH may be a different installation.
py = sys.executable
run_checked(f'"{py}" -m pip install build')
run_checked(f'"{py}" -m build')

# This version only. A bare prefix such as `0.5.8*` would also match `0.5.80`.
# The sdist is `name-version.tar.gz`; wheels are `name-version-...whl`.
dist_dir = Path('dist')
prefix = f'os_script-{version}'
artifacts = file_list_sort_by_name(find(dist_dir, f'{prefix}*'))
artifacts = [
    path for path in artifacts
    if path.name == f'{prefix}.tar.gz' or path.name.startswith(prefix + '-')
]
wheel_files = [path for path in artifacts if path.suffix == '.whl']

# Install the wheel just built, replacing any older copy already present in this environment.
if wheel_files:
    wheel_file = wheel_files[0]
    print(f'Installing version: {wheel_file}')
    run_checked(f'"{py}" -m pip install "{wheel_file}" --force-reinstall')
else:
    print(f'Wheel file matching os_script-{version}-*.whl not found in {dist_dir}')
    exit(1)

# Upload those same files only when asked. PyPI keeps every uploaded version, so older files in dist/ must not be sent again.
if args.public:
    if not artifacts:
        print(f'No distribution files for version {version} in {dist_dir}')
        exit(1)
    print('Uploading to PyPI:', ', '.join(str(path) for path in artifacts))
    run_checked(f'"{py}" -m pip install twine')
    quoted = ' '.join(f'"{path}"' for path in artifacts)
    run_checked(f'"{py}" -m twine upload {quoted}')
