import unittest
from src.html_parser.syn_groups import *
from src.html_parser.syn_parser import SynParser
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
                        {"line": [{"syn": "perform"}, {"syn": "accomplish"}, {"syn": "achieve"}, {"syn": "carry out"},
                                  {"syn": "complete"}, {"syn": "execute"}]},
                        {"line": [{"syn": "be adequate"}, {"syn": "be sufficient"}, {"syn": "cut the mustard"},
                                  {"syn": "pass muster"}, {"syn": "satisfy"}, {"syn": "suffice"}]},
                        {"line": [{"syn": "get ready"}, {"syn": "arrange"}, {"syn": "fix"}, {"syn": "look after"},
                                  {"syn": "prepare"}, {"syn": "see to"}]},
                        {"line": [{"syn": "solve"}, {"syn": "decipher"}, {"syn": "decode"}, {"syn": "figure out"},
                                  {"syn": "puzzle out"}, {"syn": "resolve"}, {"syn": "work out"}]},
                        {"line": [{"syn": "cause"}, {"syn": "bring about"}, {"syn": "create"}, {"syn": "effect"},
                                  {"syn": "produce"}]}
                    ]
                }},
                {"gram_group": {
                    "value": "noun",
                    "synonyms": [
                        {
                            "category": "informal mainly British New Zealand",
                            "line": [
                                {"syn": "event"}, {"syn": "affair"}, {"syn": "function"}, {"syn": "gathering"},
                                {"syn": "occasion"}, {"syn": "party"}]},
                    ]
                }}
            ]}
        ])

    def test_first_syngroup_returns_2_gram_groups(self):
        root = etree.HTML(self.html_content)
        dict_parser = SynParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]

        group = SynGroup(dict_parser, def_group)
        group.build()
        result = group.translate()

        self.assertEqual({"word": "do", "gram_groups": [
            {"gram_group": {
                "value": "verb",
                "synonyms": [
                    {"line": [{"syn": "perform"}, {"syn": "accomplish"}, {"syn": "achieve"}, {"syn": "carry out"},
                              {"syn": "complete"}, {"syn": "execute"}]},
                    {"line": [{"syn": "be adequate"}, {"syn": "be sufficient"}, {"syn": "cut the mustard"},
                              {"syn": "pass muster"}, {"syn": "satisfy"}, {"syn": "suffice"}]},
                    {"line": [{"syn": "get ready"}, {"syn": "arrange"}, {"syn": "fix"}, {"syn": "look after"},
                              {"syn": "prepare"}, {"syn": "see to"}]},
                    {"line": [{"syn": "solve"}, {"syn": "decipher"}, {"syn": "decode"}, {"syn": "figure out"},
                              {"syn": "puzzle out"}, {"syn": "resolve"}, {"syn": "work out"}]},
                    {"line": [{"syn": "cause"}, {"syn": "bring about"}, {"syn": "create"}, {"syn": "effect"},
                              {"syn": "produce"}]}
                ]
            }},
            {"gram_group": {
                "value": "noun",
                "synonyms": [
                    {
                        "category": "informal mainly British New Zealand",
                        "line": [
                            {"syn": "event"}, {"syn": "affair"}, {"syn": "function"}, {"syn": "gathering"},
                            {"syn": "occasion"}, {"syn": "party"}]},
                ]
            }}
        ]}, result)

    def test_first_gram_group_returns_empty_synonyms(self):
        root = etree.HTML(self.html_content)
        dict_parser = SynParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[0]

        group = SynGramGroup(dict_parser, gram_group)
        group.build()
        result = group.translate()
        self.assertEqual({"gram_group": {
            "value": "verb",
            "synonyms": [
                {"line": [{"syn": "perform"}, {"syn": "accomplish"}, {"syn": "achieve"}, {"syn": "carry out"},
                          {"syn": "complete"}, {"syn": "execute"}]},
                {"line": [{"syn": "be adequate"}, {"syn": "be sufficient"}, {"syn": "cut the mustard"},
                          {"syn": "pass muster"}, {"syn": "satisfy"}, {"syn": "suffice"}]},
                {"line": [{"syn": "get ready"}, {"syn": "arrange"}, {"syn": "fix"}, {"syn": "look after"},
                          {"syn": "prepare"}, {"syn": "see to"}]},
                {"line": [{"syn": "solve"}, {"syn": "decipher"}, {"syn": "decode"}, {"syn": "figure out"},
                          {"syn": "puzzle out"}, {"syn": "resolve"}, {"syn": "work out"}]},
                {"line": [{"syn": "cause"}, {"syn": "bring about"}, {"syn": "create"}, {"syn": "effect"},
                          {"syn": "produce"}]}
            ]
        }}, result)

    def test_1st_syn_group_list1_returns_items(self):
        root = etree.HTML(self.html_content)
        dict_parser = SynParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[0]
        sslist = dict_parser.get_senselist(gram_group)
        sslitem = dict_parser.get_all_senselist_items(sslist)[0]

        group = SynListGroup(dict_parser, sslitem)
        group.build()
        result = group.translate()
        self.assertEqual({"line": [{"syn": "perform"}, {"syn": "accomplish"}, {"syn": "achieve"}, {"syn": "carry out"},
                                   {"syn": "complete"}, {"syn": "execute"}]}, result)

    def test_1st_syn_group_returns_5_filled_lists(self):
        root = etree.HTML(self.html_content)
        dict_parser = SynParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[0]

        group = SynSenseListGroup(dict_parser, gram_group)
        group.build()
        result = group.translate()
        self.assertEqual([
            {"line": [{"syn": "perform"}, {"syn": "accomplish"}, {"syn": "achieve"}, {"syn": "carry out"}, {"syn": "complete"}, {"syn": "execute"}]},
            {"line": [{"syn": "be adequate"}, {"syn": "be sufficient"}, {"syn": "cut the mustard"}, {"syn": "pass muster"}, {"syn": "satisfy"}, {"syn": "suffice"}]},
            {"line": [{"syn": "get ready"}, {"syn": "arrange"}, {"syn": "fix"}, {"syn": "look after"}, {"syn": "prepare"}, {"syn": "see to"}]},
            {"line": [{"syn": "solve"}, {"syn": "decipher"}, {"syn": "decode"}, {"syn": "figure out"}, {"syn": "puzzle out"}, {"syn": "resolve"}, {"syn": "work out"}]},
            {"line": [{"syn": "cause"}, {"syn": "bring about"}, {"syn": "create"}, {"syn": "effect"}, {"syn": "produce"}]}
        ], result)

if __name__ == '__main__':
    unittest.main()
