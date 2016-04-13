import json
import os
import unittest
from unittest import mock
from unittest.mock import patch

from src.json_reader import JsonReader, DefGroupReader


class TestJsonReader(unittest.TestCase):
    content_text = None
    content_json = None
    dir_path = "./test-data"

    @classmethod
    def setUpClass(cls):
        TestJsonReader.expected_json = None
        TestJsonReader.expected_print = None

        os.chdir("./do")
        exp_json = "expected_do.json"
        exp_print = "expected_do.txt"

        with open(exp_json, "r") as f:
            TestJsonReader.content_json = json.load(f)

        with open(exp_print, "r") as f:
            TestJsonReader.content_text = f.read()

        os.makedirs(TestJsonReader.dir_path, exist_ok=True)

    def setUp(self):
        self.word = "do"

    @unittest.skip("SKIP ---- not yet impl")
    def test_jsonToText_returnsAll(self):
        cmd = JsonReader(TestJsonReader.content_json)

        text = cmd.read_content(TestJsonReader.content_json)

        self.assertEqual(text, TestJsonReader.content_text)

    def test_toText_frequency(self):
        cmd = JsonReader(TestJsonReader.content_json)

        text = cmd.frequency()

        self.assertEqual(text, "[Extremely Common]\n\n")

    def test_toText_Definitions(self):
        cmd = JsonReader(TestJsonReader.content_json)

        with patch.object(DefGroupReader, "read_def_group") as mock_ggroups:
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
