import json
import os

import unittest

from src.html_parser import HtmlParser


class HtmlParserTest(unittest.TestCase):
    def_expected_json = None
    learn_expected_json = None
    def_html_content = None

    syn_expected_json = None
    syn_html_content = None

    @classmethod
    def setUpClass(cls):
        path = os.path.dirname(os.path.abspath(__file__))
        learn_json_file_name = os.path.join(path, "expected_do.learn")
        def_json_file_name = os.path.join(path, "expected_do.def")
        html_path = os.path.join(path, "html_files")

        html_file_name = os.path.join(path, html_path, "do_defs.html")

        syn_json_file_name = os.path.join(path, "expected_do.syn")
        syn_html_file_name = os.path.join(path, html_path, "do_syn.html")

        with open(learn_json_file_name) as f:
            cls.learn_expected_json = json.load(f)

        with open(def_json_file_name) as f:
            cls.def_expected_json = json.load(f)

        with open(html_file_name) as f:
            cls.def_html_content = f.read()

        with open(syn_json_file_name) as f:
            cls.syn_expected_json = json.load(f)

        with open(syn_html_file_name) as f:
            cls.syn_html_content = f.read()

    def test_htmlParse_do(self):
        parser = HtmlParser()
        result = parser.parse("do", HtmlParserTest.def_html_content)

        self.assertEqual(HtmlParserTest.def_expected_json, result)

    def test_htmlParse_syn_do(self):
        parser = HtmlParser()
        result = parser.parse_syn("do", HtmlParserTest.syn_html_content)

        self.assertEqual(HtmlParserTest.syn_expected_json, result)

    def test_htmlParse_learn_do(self):
        parser = HtmlParser()
        result = parser.parse_learn("do", HtmlParserTest.def_html_content)

        self.assertEqual(HtmlParserTest.learn_expected_json, result)


if __name__ == '__main__':
    unittest.main()
