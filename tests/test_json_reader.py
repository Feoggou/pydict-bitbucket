import json
import os
import unittest
from unittest import mock
from unittest.mock import patch

from src.json_reader import JsonReader


class TestJsonReader(unittest.TestCase):
    word_exp_print = None
    word_exp_json = None
    dir_path = "./test-data"

    @classmethod
    def setUpClass(cls):
        TestJsonReader.expected_json = None
        TestJsonReader.expected_print = None

        os.chdir("./do")
        exp_json = "expected_do.json"
        exp_print = "expected_do.txt"

        with open(exp_json, "r") as f:
            TestJsonReader.word_exp_json = json.load(f)

        with open(exp_print, "r") as f:
            TestJsonReader.word_exp_print = f.read()

        os.makedirs(TestJsonReader.dir_path, exist_ok=True)

    def setUp(self):
        self.word = "do"

    @unittest.skip("SKIP ---- not yet impl")
    def test_jsonToText_returnsAll(self):
        cmd = JsonReader(TestJsonReader.word_exp_json)

        text = cmd.read_content(TestJsonReader.word_exp_json)

        self.assertEqual(text, TestJsonReader.word_exp_print)

    def test_toText_frequency(self):
        cmd = JsonReader(TestJsonReader.word_exp_json)

        text = cmd.frequency()

        self.assertEqual(text, "[Extremely Common]\n\n")

    def test_toText_Definitions(self):
        cmd = JsonReader(TestJsonReader.word_exp_json)

        with patch.object(JsonReader, "_read_gram_groups") as mock_ggroups:
            mock_ggroups.side_effect = ["group1\n", "group2\n", "group3\n", "group4\n", "group5\n"]

            text = cmd.definitions()

        self.assertEqual(text, "DEFINTIONS\n"
                               "group1\n"
                               "group2\n"
                               "group3\n"
                               "group4\n"
                               "group5\n\n")

if __name__ == "__main__":
    unittest.main()
