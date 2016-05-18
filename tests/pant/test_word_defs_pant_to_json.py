import unittest
from unittest.mock import patch
from src.html_parser.def_groups import *
from src.html_parser.def_parser import DefParser
from lxml import etree


class HtmlToJsonTest(unittest.TestCase):

    def setUp(self):
        f = open("pant_defs.html")
        self.word_name = "pant"

        self.html_content = f.read()

    def test_second_def_group_returns_full_content(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[1]

        group = DefGroup(dict_parser, def_group)
        group.build()
        result = group.translate()
        print(result)

        self.assertEqual(
            {"word": "pant", "gram_groups": [
                {
                    "value": "noun adjective",
                    "defs": [{"def": "see pants[1]"}]
                },
            ]}, result)

if __name__ == '__main__':
    unittest.main()
