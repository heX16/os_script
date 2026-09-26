# coding: utf-8
# Simple installer for BOSL2 OpenSCAD library.
# https://github.com/BelfrySCAD/BOSL2/

import os
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

try:
    from pyshellscript import *
except ImportError:
    sys.path.insert(0, r'H:\Pyt\pyshellscript')
    from pyshellscript import *

BOSL2_ZIP_URL = 'https://github.com/BelfrySCAD/BOSL2/archive/refs/heads/master.zip'

_pyss_mv = mv


def get_openscad_library_path() -> Path:
    # Prefer OPENSCADPATH if set (covers SNAP and custom installs).
    env_path = os.environ.get('OPENSCADPATH')
    if env_path:
        return Path(env_path)

    home = Path.home()
    if is_wnd():
        return home / 'Documents' / 'OpenSCAD' / 'libraries'
    if is_linux():
        return home / '.local' / 'share' / 'OpenSCAD' / 'libraries'
    # macOS and other Unix-like
    return home / 'Documents' / 'OpenSCAD' / 'libraries'


def find_extracted_root(extract_dir: Path) -> Path:
    # Archive root is usually BOSL2-master or BOSL-v2.0.
    for name in ('BOSL2-master', 'BOSL-v2.0'):
        candidate = extract_dir / name
        if candidate.is_dir():
            return candidate

    dirs = [p for p in extract_dir.iterdir() if p.is_dir()]
    if len(dirs) == 1:
        return dirs[0]
    raise RuntimeError(f'Cannot find BOSL2 root in {extract_dir}')


def mkdir_p(path: Path) -> None:
    print(f'mkdir -p {path}')
    path.mkdir(parents=True, exist_ok=True)


def download(url: str, dest: Path) -> None:
    print(f'Downloading {url}...')
    urllib.request.urlretrieve(url, dest)


def unzip(zip_path: Path, extract_dir: Path) -> None:
    print(f'unzip {zip_path} -> {extract_dir}')
    extract_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zf.extractall(extract_dir)


def rm_rf(path: Path) -> None:
    if not path.exists():
        return
    print(f'rm -rf {path}')
    rmdir(path, recursive=True)


def mv(source: Path | str, destination: Path | str) -> None:
    print(f'mv {source} -> {destination}')
    _pyss_mv(source, destination)


def install_bosl2() -> None:
    lib_path = get_openscad_library_path()
    target_dir = lib_path / 'BOSL2'

    with tempfile.TemporaryDirectory(prefix='bosl2_install_') as tmp:
        tmp_dir = Path(tmp)
        zip_path = tmp_dir / 'BOSL2_master.zip'
        extract_dir_tmp = tmp_dir / 'extract'

        mkdir_p(lib_path)
        download(BOSL2_ZIP_URL, zip_path)
        unzip(zip_path, extract_dir_tmp)
        rm_rf(target_dir)
        mv(find_extracted_root(extract_dir_tmp), target_dir)

    print(f'Done. BOSL2 installed to: {target_dir}')
    print('Restart OpenSCAD to use the library.')


if __name__ == '__main__':
    try:
        install_bosl2()
    except Exception as e:
        print(f'Install failed: {e}')
        sys.exit(1)
