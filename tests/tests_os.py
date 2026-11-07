import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import mock_open, patch

from os_script import *


def _env_without_snap():
    return {key: value for key, value in os.environ.items() if key not in ('SNAP', 'SNAP_NAME')}


class TestIsSnap(unittest.TestCase):
    """`is_snap()`"""

    def test_snap_env(self):
        with patch.dict(os.environ, {'SNAP': '/snap/app'}):
            self.assertTrue(is_snap())

    def test_snap_name_env(self):
        with patch.dict(os.environ, {**_env_without_snap(), 'SNAP_NAME': 'app'}, clear=True):
            self.assertTrue(is_snap())

    def test_cgroup(self):
        with patch.dict(os.environ, _env_without_snap(), clear=True):
            with patch('builtins.open', mock_open(read_data='0::/user.slice/snap.foo\n')):
                self.assertTrue(is_snap())

    def test_not_snap(self):
        with patch.dict(os.environ, _env_without_snap(), clear=True):
            with patch('builtins.open', mock_open(read_data='0::/user.slice/user-1000.slice\n')):
                self.assertFalse(is_snap())

    def test_cgroup_oserror(self):
        with patch.dict(os.environ, _env_without_snap(), clear=True):
            with patch('builtins.open', side_effect=OSError):
                self.assertFalse(is_snap())


class TestIsMounted(unittest.TestCase):
    """`is_mounted(...)`"""

    def test_root_is_mounted(self):
        if is_wnd():
            self.skipTest('POSIX root mount check')
        self.assertTrue(is_mounted('/'))

    def test_fresh_dir_is_not_mounted(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertFalse(is_mounted(tmp))
            self.assertFalse(is_mounted(Path(tmp)))

    def test_missing_path_is_not_mounted(self):
        missing = Path(tempfile.gettempdir()) / 'os_script_not_a_mount_point'
        self.assertFalse(missing.exists())
        self.assertFalse(is_mounted(missing))


class TestSameFs(unittest.TestCase):
    """`same_fs(...)`"""

    def test_not_linux(self):
        if is_linux():
            self.skipTest('non-Linux check')
        with self.assertRaises(RuntimeError):
            same_fs('.', '.')

    def test_nested_dir_is_same_fs(self):
        if not is_linux():
            self.skipTest('Linux only')
        with tempfile.TemporaryDirectory() as tmp:
            nested = Path(tmp) / 'nested'
            nested.mkdir()
            self.assertTrue(same_fs(tmp, nested))
            self.assertTrue(same_fs(Path(tmp), nested))

    def test_missing_path(self):
        if not is_linux():
            self.skipTest('Linux only')
        missing = Path(tempfile.gettempdir()) / 'os_script_same_fs_missing'
        self.assertFalse(missing.exists())
        with self.assertRaises(FileNotFoundError):
            same_fs(missing, tempfile.gettempdir())


if __name__ == '__main__':
    unittest.main()
