import unittest
from src.def_groups import *
from src.dict_parse import DictSynParser
from src.html_to_json import HtmlToJsonSynonyms
from lxml import etree


class HtmlToJsonSynTest(unittest.TestCase):
    def setUp(self):
        f = open("do_syn.html")
        self.word_name = "do"
        self.html_content = f.read()
        self.maxDiff = None

    def test_create_html_to_json_obj(self):
        obj = HtmlToJsonSynonyms(self.word_name, self.html_content)
        self.assertIsNotNone(obj)

    def test_return_all(self):
        obj = HtmlToJsonSynonyms(self.word_name, self.html_content)

        json_obj = obj.translate()
        self.assertEqual(json_obj, [
            {"word": "do", "gram_groups": [
                {"gram_group": {
                    "value": "verb",
                    "synonyms": [
                        {"line": ["perform", "accomplish", "achieve", "carry out", "complete", "execute"]},
                        {"line": ["be adequate", "be sufficient", "cut the mustard", "pass muster", "satisfy", "suffice"]},
                        {"line": ["get ready", "arrange", "fix", "look after", "prepare", "see to"]},
                        {"line": ["solve", "decipher", "decode", "figure out", "puzzle out", "resolve", "work out"]},
                        {"line": ["cause", "bring about", "create", "effect", "produce"]}
                    ]
                }},
                {"gram_group": {
                    "value": "noun",
                    "synonyms": [
                        {"category": "informal mainly British New Zealand",
                         "line": [
                             "event", "affair", "function", "gathering", "occasion", "party"]
                         },
                    ]
                }}
            ]}
        ])

    def test_first_syngroup_returns_2_gram_groups(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictSynParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]

        group = SynGroup(dict_parser, def_group)
        group.build()
        result = group.translate()
        self.assertEqual({"word": "do", "gram_groups": [
            {"gram_group": {
                "value": "verb",
                "synonyms": [
                    {"line": ["perform", "accomplish", "achieve", "carry out", "complete", "execute"]},
                    {"line": ["be adequate", "be sufficient", "cut the mustard", "pass muster", "satisfy", "suffice"]},
                    {"line": ["get ready", "arrange", "fix", "look after", "prepare", "see to"]},
                    {"line": ["solve", "decipher", "decode", "figure out", "puzzle out", "resolve", "work out"]},
                    {"line": ["cause", "bring about", "create", "effect", "produce"]}
                ]
            }},
            {"gram_group": {
                "value": "noun",
                "synonyms": [
                    {"category": "informal mainly British New Zealand",
                     "line": ["event", "affair", "function", "gathering", "occasion", "party"]},
                ]
            }}
        ]}, result)

    def test_first_gram_group_returns_empty_synonyms(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictSynParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[0]

        group = SynGramGroup(dict_parser, gram_group)
        group.build()
        result = group.translate()
        self.assertEqual({"gram_group": {
            "value": "verb",
            "synonyms": [
                {"line": ["perform", "accomplish", "achieve", "carry out", "complete", "execute"]},
                {"line": ["be adequate", "be sufficient", "cut the mustard", "pass muster", "satisfy", "suffice"]},
                {"line": ["get ready", "arrange", "fix", "look after", "prepare", "see to"]},
                {"line": ["solve", "decipher", "decode", "figure out", "puzzle out", "resolve", "work out"]},
                {"line": ["cause", "bring about", "create", "effect", "produce"]}
            ]
        }}, result)

    def test_1st_syn_group_list1_returns_items(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictSynParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[0]
        sslist = dict_parser.get_senselist(gram_group)
        sslitem = dict_parser.get_all_senselist_items(sslist)[0]

        group = SynListGroup(dict_parser, sslitem)
        group.build()
        result = group.translate()
        self.assertEqual({"line": ["perform", "accomplish", "achieve", "carry out", "complete", "execute"]}, result)

    def test_1st_syn_group_returns_5_filled_lists(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictSynParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[0]

        group = SynSenseListGroup(dict_parser, gram_group)
        group.build()
        result = group.translate()
        self.assertEqual([
            {"line": ["perform", "accomplish", "achieve", "carry out", "complete", "execute"]},
            {"line": ["be adequate", "be sufficient", "cut the mustard", "pass muster", "satisfy", "suffice"]},
            {"line": ["get ready", "arrange", "fix", "look after", "prepare", "see to"]},
            {"line": ["solve", "decipher", "decode", "figure out", "puzzle out", "resolve", "work out"]},
            {"line": ["cause", "bring about", "create", "effect", "produce"]}
        ], result)

if __name__ == '__main__':
    unittest.main()
