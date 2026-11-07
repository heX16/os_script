import sys
import tempfile
import unittest
from pathlib import Path

from os_script import *
from os_script.os_script import _set_global_variables


class TestLoadFromJsonStream(unittest.TestCase):
    """`load_from_json_stream(...)`"""

    def test_ndjson(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'records.jsonl'
            path.write_text('{"a": 1}\n{"b": 2}\n', encoding='utf-8')
            self.assertEqual(load_from_json_stream(path), [{'a': 1}, {'b': 2}])

    def test_concatenated_pretty_objects(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'records.json'
            path.write_text('{\n  "a": 1\n}\n{\n  "b": 2\n}\n', encoding='utf-8')
            self.assertEqual(load_from_json_stream(path), [{'a': 1}, {'b': 2}])


class TestJsonIterRecords(unittest.TestCase):
    """`json_iter_records(...)`"""

    def test_nested_records(self):
        data = {
            'meta': {'id': 1},
            'items': [
                {'name': 'a', 'nested': [{'hidden': True}]},
                [{'name': 'b'}],
                'skip',
            ],
        }
        records = list(json_iter_records(data))
        self.assertEqual(records, [
            {'name': 'a', 'nested': [{'hidden': True}]},
            {'name': 'b'},
        ])


class TestDictCastValuesBool(unittest.TestCase):
    """String booleans in `dict_cast_values(...)`."""

    def test_false_string(self):
        casted = dict_cast_values(
            {'debug': 'false', 'verbose': 'true'},
            {'debug': False, 'verbose': True},
        )
        self.assertIs(casted['debug'], False)
        self.assertIs(casted['verbose'], True)


# Module-level names used by TestSetGlobalVariablesCallerNamespace
_cfg_declared_retries = 0
_cfg_declared_timeout = 0.0
_cfg_declared_label = None


class TestSetGlobalVariables(unittest.TestCase):
    """`_set_global_variables(...)` type and existence filters."""

    def test_skip_undeclared_name(self):
        namespace = {'retries': 0}
        _set_global_variables({'retries': 3, 'extra': 'ignored'}, namespace)
        self.assertEqual(namespace, {'retries': 3})
        self.assertNotIn('extra', namespace)

    def test_exact_type(self):
        namespace = {'debug': False, 'retries': 0, 'name': ''}
        _set_global_variables(
            {'debug': True, 'retries': 5, 'name': 'app'},
            namespace,
        )
        self.assertIs(namespace['debug'], True)
        self.assertEqual(namespace['retries'], 5)
        self.assertEqual(namespace['name'], 'app')

    def test_incompatible_type_skipped(self):
        namespace = {'retries': 'zero'}
        _set_global_variables({'retries': 3}, namespace)
        self.assertEqual(namespace['retries'], 'zero')

    def test_none_accepts_any_type(self):
        namespace = {'label': None, 'count': None}
        _set_global_variables({'label': 'ready', 'count': 7}, namespace)
        self.assertEqual(namespace['label'], 'ready')
        self.assertEqual(namespace['count'], 7)

    def test_float_accepts_int(self):
        namespace = {'timeout': 0.0}
        _set_global_variables({'timeout': 2}, namespace)
        self.assertEqual(namespace['timeout'], 2.0)
        self.assertIs(type(namespace['timeout']), float)

    def test_int_rejects_bool_and_float(self):
        namespace = {'retries': 0, 'limit': 1}
        _set_global_variables({'retries': True, 'limit': 1.5}, namespace)
        self.assertEqual(namespace['retries'], 0)
        self.assertEqual(namespace['limit'], 1)

    def test_bool_accepts_int_and_strings(self):
        namespace = {
            'a': False, 'b': False, 'c': False, 'd': True,
            'e': False, 'f': True, 'g': False, 'h': True,
            'skip': False,
        }
        _set_global_variables(
            {
                'a': 1, 'b': 0, 'c': True, 'd': False,
                'e': 'true', 'f': 'false', 'g': 'yes', 'h': 'NO',
                'skip': 2,
            },
            namespace,
        )
        self.assertIs(namespace['a'], True)
        self.assertIs(namespace['b'], False)
        self.assertIs(namespace['c'], True)
        self.assertIs(namespace['d'], False)
        self.assertIs(namespace['e'], True)
        self.assertIs(namespace['f'], False)
        self.assertIs(namespace['g'], True)
        self.assertIs(namespace['h'], False)
        self.assertIs(namespace['skip'], False)


class TestSetGlobalVariablesCallerNamespace(unittest.TestCase):
    """Config loaders write into the caller module globals."""

    def _assert_caller_globals_updated(self):
        self.assertEqual(_cfg_declared_retries, 9)
        self.assertEqual(_cfg_declared_timeout, 1.0)
        self.assertIs(type(_cfg_declared_timeout), float)
        self.assertEqual(_cfg_declared_label, 'ok')
        self.assertFalse(hasattr(sys.modules[__name__], '_cfg_undeclared_extra'))
        self.assertFalse(hasattr(sys.modules['os_script.os_script'], '_cfg_undeclared_extra'))
        self.assertFalse(hasattr(sys.modules['os_script.os_script'], '_cfg_declared_retries'))

    def test_load_config_from_json_updates_caller_globals_only(self):
        global _cfg_declared_retries, _cfg_declared_timeout, _cfg_declared_label

        _cfg_declared_retries = 0
        _cfg_declared_timeout = 0.0
        _cfg_declared_label = None

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'config.json'
            path.write_text(
                '{"_cfg_declared_retries": 9, "_cfg_declared_timeout": 1, '
                '"_cfg_declared_label": "ok", "_cfg_undeclared_extra": "x"}',
                encoding='utf-8',
            )
            load_config_from_json(path, {
                '_cfg_declared_retries': 0,
                '_cfg_declared_timeout': 0.0,
                '_cfg_declared_label': '',
                '_cfg_undeclared_extra': 'ignored',
            })

        self._assert_caller_globals_updated()

    def test_load_config_from_dict_updates_caller_globals_only(self):
        global _cfg_declared_retries, _cfg_declared_timeout, _cfg_declared_label

        _cfg_declared_retries = 0
        _cfg_declared_timeout = 0.0
        _cfg_declared_label = None

        load_config_from_dict(
            {
                '_cfg_declared_retries': 9,
                '_cfg_declared_timeout': 1,
                '_cfg_declared_label': 'ok',
                '_cfg_undeclared_extra': 'x',
            },
            {
                '_cfg_declared_retries': 0,
                '_cfg_declared_timeout': 0.0,
                '_cfg_declared_label': '',
                '_cfg_undeclared_extra': 'ignored',
            },
        )

        self._assert_caller_globals_updated()


if __name__ == '__main__':
    unittest.main()
