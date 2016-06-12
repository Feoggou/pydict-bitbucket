import json
import os

import unittest

from src.html_parser import HtmlParser


class HtmlParserTest(unittest.TestCase):
    expected_json = None
    html_content = None

    @classmethod
    def setUpClass(cls):
        path = os.path.dirname(os.path.abspath(__file__))
        json_file_name = os.path.join(path, "expected_do.def")
        html_file_name = os.path.join(path, "do", "do_defs.html")

        with open(json_file_name) as f:
            cls.expected_json = json.load(f)

        with open(html_file_name) as f:
            cls.html_content = f.read()

    def test_htmlParse_do(self):
        parser = HtmlParser()
        result = parser.parse("do", HtmlParserTest.html_content)

        self.assertEqual(HtmlParserTest.expected_json, result)


if __name__ == '__main__':
    unittest.main()
