import json
import os

import unittest

from src.json_reader import JsonReader
from src.json_learn_reader import JsonLearnReader
from src.json_syn_reader import JsonSynReader


class JsonReaderTest(unittest.TestCase):
    def_json = None
    def_txt = None
    learn_json = None
    learn_txt = None

    syn_json = None
    syn_txt = None

    @classmethod
    def setUpClass(cls):
        path = os.path.dirname(os.path.abspath(__file__))
        learn_json_file_name = os.path.join(path, "expected_do.learn")
        def_json_file_name = os.path.join(path, "expected_do.def")
        def_txt_file_name = os.path.join(path, "expected_do.txt")
        learn_txt_file_name = os.path.join(path, "expected_do_learn.txt")

        syn_json_file_name = os.path.join(path, "expected_do.syn")
        syn_txt_file_name = os.path.join(path, "expected_do_syn.txt")

        with open(learn_json_file_name) as f:
            cls.learn_json = json.load(f)

        with open(def_json_file_name) as f:
            cls.def_json = json.load(f)

        with open(def_txt_file_name) as f:
            cls.def_txt = f.read()

        with open(learn_txt_file_name) as f:
            cls.learn_txt = f.read()

        with open(syn_json_file_name) as f:
            cls.syn_json = json.load(f)

        with open(syn_txt_file_name) as f:
            cls.syn_txt = f.read()

    def test_jsonRead_do(self):
        reader = JsonReader(JsonReaderTest.def_json, use_colors=False)
        actual = reader.read_content("do")

        self.assertEqual(JsonReaderTest.def_txt, actual)

    def test_jsonLearnRead_do(self):
        reader = JsonLearnReader(JsonReaderTest.learn_json, use_colors=False)
        actual = reader.read_content()

        self.assertEqual(JsonReaderTest.learn_txt, actual)

    def test_jsonSynRead_do(self):
        reader = JsonSynReader(JsonReaderTest.syn_json, use_colors=False)
        actual = reader.read_content()

        self.assertEqual(JsonReaderTest.syn_txt, actual)


if __name__ == '__main__':
    unittest.main()
