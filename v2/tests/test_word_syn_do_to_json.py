import unittest
import os

from unittest.mock import patch
from src.syn_groups import *
from src.syn_parser import SynParser
from lxml import etree

from src.html_parser import HtmlParser
from src import config


class HtmlToJsonTest(unittest.TestCase):
    word_name = ""
    html_content = ""

    @classmethod
    def setUpClass(cls):
        file_name = os.path.join(config.HTML_SOURCE_PATH, "do_syn.html")

        with open(file_name) as f:
            cls.word_name = "do"
            cls.html_content = f.read()

    def test_createHtmlToJson_obj(self):
        obj = HtmlParser()
        self.assertIsNotNone(obj)

    def test_synDefGroup_returnsEmpty(self):
        root = etree.HTML(self.html_content)
        dict_parser = SynParser(root, self.word_name)

        with patch.object(SynDefGroup, 'build'):
            group = SynDefGroup(dict_parser)
            group.build()
            result = group.translate()
            self.assertEqual({'gram_groups': [], 'word': 'do'}, result)

    def test_defGroup0_returns_2_gramGroups(self):
        root = etree.HTML(self.html_content)
        dict_parser = SynParser(root, self.word_name)

        with patch.object(SynGramGroup, 'build'):
            group = SynDefGroup(dict_parser)
            group.build()
            result = group.translate()

            self.assertEqual({"word": "do", "gram_groups": [{}, {}]},
                             result)

    def test_syn(self):
        root = etree.HTML(self.html_content)
        dict_parser = SynParser(root, self.word_name)
        gram_group = dict_parser.get_all_grammar_groups()[0]
        sense = dict_parser.get_all_sense_items(gram_group)[0]

        word = SynLine(dict_parser, sense)
        word.build()
        result = word.translate()

        self.assertEqual({
            "syn_line": [
                {"perform": ""}, {"work": ""}, {"achieve": ""}, {"carry out": ""}, {"produce": ""}, {"effect": ""},
                {"complete": ""}, {"conclude": ""}, {"undertake": ""}, {"accomplish": ""}, {"execute": ""},
                {"discharge": ""}, {"pull off": ""}, {"transact": ""}
            ],
            "example": "I was trying to do some work.",
            "mark": "good"
        }, result)

    """def test_gramGroup0_fullContent(self):
        root = etree.HTML(self.html_content)
        dict_parser = SynParser(root, self.word_name)
        gram_group = dict_parser.get_all_grammar_groups()[0]

        group = SynGramGroup(dict_parser, gram_group)
        group.build()
        result = group.translate()

        print(result)

        self.assertEqual({
            "value": "verb",
            "syns": [
                {
                    "syn_line": {
                        "perform": "", "work": "", "achieve": "", "carry out": "", "produce": "", "effect": "",
                        "complete": "", "conclude": "", "undertake": "", "accomplish": "", "execute": "",
                        "discharge": "", "pull off": "", "transact": ""
                    },
                    "example": "I was trying to do some work.",
                    "mark": "good"
                }
            ]
        }, result)

    def test_gramGroup1_fullContent(self):
        root = etree.HTML(self.html_content)
        dict_parser = SynParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[1]

        group = GramGroup(dict_parser, gram_group)
        group.build()
        result = group.translate()

        self.assertEqual({
            "forms": {"items": ["dos", "do's"], "info": "plural"},
            "value": "noun",
            "defs": {
                "": [
                    {"category": "slang", "def": "an act or instance of cheating or swindling", "mark": "good"},
                    {
                        "category": "informal, mainly British and New Zealand",
                        "def": "a formal or festive gathering; party",
                        "mark": "good"
                    },
                    {"def": "(i) See do's and don'ts", "mark": "good"},
                ]
            }
        }, result)

    def test_defGroup0_fullContent(self):
        root = etree.HTML(self.html_content)
        dict_parser = SynParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[1]

        group = DefGroup(dict_parser, def_group)
        group.build()
        result = group.translate()

        self.assertEqual(
            {"word": "do or do a",
             "frequency": "",
             "gram_groups": [
                 {
                     "forms": {"items": [], "info": ""},
                     "defs": {
                         "": [
                             {
                                 "category": "informal",
                                 "def": "to act like; imitate",
                                 "example": "he's a good mimic – he can do all his friends well",
                                 "mark": "good"
                             },
                         ],
                     }
                 },
             ]}, result)"""

if __name__ == '__main__':
    unittest.main()
