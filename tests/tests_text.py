import tempfile
import unittest
from pathlib import Path

from os_script import *


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


if __name__ == '__main__':
    unittest.main()
