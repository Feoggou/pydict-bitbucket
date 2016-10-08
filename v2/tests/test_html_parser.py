import json
import os

import unittest

from src.html_parser import HtmlParser
from src import config


class HtmlParserTest(unittest.TestCase):
    tests_path = None

    @classmethod
    def read_content(cls, html_file, json_file):
        json_file_name = os.path.join(cls.tests_path, "json_files", json_file)
        html_file_name = os.path.join(config.HTML_SOURCE_PATH, html_file)

        with open(json_file_name) as f:
            expected_json = json.load(f)

        with open(html_file_name) as f:
            html_content = f.read()

        return html_content, expected_json

    @classmethod
    def setUpClass(cls):
        cls.tests_path = os.path.dirname(os.path.abspath(__file__))

    def test_htmlParse_do(self):
        html_contant, exp_json = self.read_content("do_defs.html", "expected_do.def")

        parser = HtmlParser()
        result = parser.parse("do", html_contant)

        self.assertEqual(exp_json, result)

    def test_htmlParse_syn_do(self):
        html_contant, exp_json = self.read_content("do_syn.html", "expected_do.syn")

        parser = HtmlParser()
        result = parser.parse_syn("do", html_contant)

        self.assertEqual(exp_json, result)

    def test_htmlParse_learn_do(self):
        html_contant, exp_json = self.read_content("do_defs.html", "expected_do.learn")

        parser = HtmlParser()
        result = parser.parse_learn("do", html_contant)

        self.assertEqual(exp_json, result)

    def test_htmlParse_tall(self):
        # has 'derived forms'
        html_contant, exp_json = self.read_content("tall_defs.html", "expected_tall.def")

        parser = HtmlParser()
        result = parser.parse("tall", html_contant)

        self.assertEqual(exp_json, result)

    def test_htmlParse_syn_tall(self):
        # has opposites
        html_contant, exp_json = self.read_content("tall_syn.html", "expected_tall.syn")

        parser = HtmlParser()
        result = parser.parse_syn("tall", html_contant)

        """saver = JsonSaver()
        saver.save("_tall.syn", result)

        # print(result)
        self.maxDiff = None"""

        self.assertEqual(exp_json, result)

    def test_htmlParse_learn_tall(self):
        # has an issue with gram values
        html_contant, exp_json = self.read_content("tall_defs.html", "expected_tall.learn")

        parser = HtmlParser()
        result = parser.parse_learn("tall", html_contant)

        self.assertEqual(exp_json, result)


if __name__ == '__main__':
    unittest.main()
