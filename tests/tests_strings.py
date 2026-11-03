import unittest

from os_script import *


class TestStrToBool(unittest.TestCase):
    """`str_to_bool(...)`"""

    def test_true_and_false_sets(self):
        for value in ('1', 'true', 'yes', 'y', 'on', 't', ' TRUE ', 'Yes'):
            self.assertIs(str_to_bool(value), True)
        for value in ('0', 'false', 'no', 'n', 'off', 'f', ' FALSE ', 'Off'):
            self.assertIs(str_to_bool(value), False)

    def test_bool_and_int_passthrough(self):
        self.assertIs(str_to_bool(True), True)
        self.assertIs(str_to_bool(False), False)
        self.assertIs(str_to_bool(1), True)
        self.assertIs(str_to_bool(0), False)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            str_to_bool('maybe')
        with self.assertRaises(ValueError):
            str_to_bool(2)
        self.assertIsNone(str_to_bool('maybe', raise_exception=False))
        self.assertIsNone(str_to_bool(2, raise_exception=False))


class TestSafeFilename(unittest.TestCase):
    """`safe_filename(...)`"""

    def test_basic(self):
        self.assertEqual(safe_filename('Hello, world!'), 'Hello world')
        self.assertEqual(safe_filename('a_b-c'), 'a_b-c')

    def test_empty_uses_default(self):
        self.assertEqual(safe_filename(None), 'untitled')
        self.assertEqual(safe_filename(''), 'untitled')
        self.assertEqual(safe_filename('***'), 'untitled')
        self.assertEqual(safe_filename('   '), 'untitled')

    def test_strip(self):
        self.assertEqual(safe_filename('  hello  '), 'hello')

    def test_custom_allowed(self):
        self.assertEqual(safe_filename('file.txt'), 'filetxt')
        self.assertEqual(safe_filename('file.txt', allowed=' _-.'), 'file.txt')


if __name__ == '__main__':
    unittest.main()
