import json
import os

import unittest

from src.json_reader import JsonReader
from src.json_learn_reader import JsonLearnReader
from src.json_syn_reader import JsonSynReader
from src import config


class JsonReaderTest(unittest.TestCase):
    tests_path = None

    @classmethod
    def read_contents(cls, json_file, txt_file):
        json_file_name = os.path.join(cls.tests_path, "json_files", json_file)
        txt_file_name = os.path.join(cls.tests_path, "txt_files", txt_file)

        with open(json_file_name) as f:
            json_file = json.load(f)

        with open(txt_file_name) as f:
            txt_file = f.read()

        return json_file, txt_file

    @classmethod
    def setUpClass(cls):
        config.USE_COLORS = False
        cls.tests_path = os.path.dirname(os.path.abspath(__file__))

    def test_jsonRead_do(self):
        json_content, exp_txt_content = self.read_contents("expected_do.def", "expected_do.txt")

        reader = JsonReader(json_content)
        actual = reader.read_content()

        self.assertEqual(exp_txt_content, actual)

    def test_jsonLearnRead_do(self):
        json_content, exp_txt_content = self.read_contents("expected_do.learn", "expected_do_learn.txt")

        reader = JsonLearnReader(json_content)
        actual = reader.read_content()

        self.assertEqual(exp_txt_content, actual)

    def test_jsonSynRead_do(self):
        json_content, exp_txt_content = self.read_contents("expected_do.syn", "expected_do_syn.txt")

        reader = JsonSynReader(json_content)
        actual = reader.read_content()

        self.assertEqual(exp_txt_content, actual)

    def test_jsonRead_tall(self):
        """has subdef, derived forms."""
        json_content, exp_txt_content = self.read_contents("expected_tall.def", "expected_tall.txt")

        reader = JsonReader(json_content)
        actual = reader.read_content()

        self.assertEqual(exp_txt_content, actual)

    def test_jsonSynRead_tall(self):
        """has opposites"""
        json_content, exp_txt_content = self.read_contents("expected_tall.syn", "expected_tall_syn.txt")

        reader = JsonSynReader(json_content)
        actual = reader.read_content()

        self.assertEqual(exp_txt_content, actual)


if __name__ == '__main__':
    unittest.main()
