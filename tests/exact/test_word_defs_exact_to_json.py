import unittest
from unittest.mock import patch
from src.def_groups import *
from src.def_parser import DictParser
from src import html_to_json
from src.html_to_json import HtmlToJson
from lxml import etree


class HtmlToJsonTest(unittest.TestCase):

    def setUp(self):
        f = open("exact_defs.html")
        self.word_name = "exact"

        self.html_content = f.read()
        # self.maxDiff = None

    def test_create_html_to_json_obj(self):
        obj = HtmlToJson(self.word_name, self.html_content)
        self.assertIsNotNone(obj)

    def test_translate_empty_main_to_json_returns_empty_word(self):
        obj = HtmlToJson(self.word_name, self.html_content)

        with patch('src.html_to_json.MainDefGroup.build_children') as mock:
            mock.return_value = None
            json_obj = obj.translate()
            html_to_json.MainDefGroup.build_children.assert_called_once_with()
            self.assertEqual(json_obj, {})

    def test_word_freq_group_value_is_extremely_common(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)

        group = WordFrequencyGroup(dict_parser)
        group.build()
        result = group.translate()
        self.assertEqual(result, "Very Common")

    # word / def_groups / def_group [0]
    def test_first_def_group_returns_no_items(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)
        etree_group = dict_parser.get_all_def_groups()[0]

        with patch('src.html_to_json.DefGroup.build') as mock:
            mock.return_value = None
            group = DefGroup(dict_parser, etree_group)
            group.build()
            result = group.translate()
            self.assertEqual({"word": "exact", "gram_groups": []}, result)

    # word / def_groups
    def test_def_groups_returns_1_def_groups(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)

        with patch('src.html_to_json.DefGroup.build'):
            group = DefGroups(dict_parser)
            group.build()
            result = group.translate()
            self.assertEqual([{"word": "exact", "gram_groups": []}], result)

    # word / def_groups / def_group [0] / gram_groups
    def test_first_def_group_returns_2_gram_groups(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]

        with patch('src.html_to_json.GramGroup.build'):
            with patch('src.html_to_json.RelatedGroup.build'):
                group = DefGroup(dict_parser, def_group)
                group.build()
                result = group.translate()
                self.assertEqual({"word": "exact",
                                  "derived_forms": {"noun": "exactness, exactor exacter", "adjective": "exactable"},
                                  "gram_groups": [{}, {}]},
                                 result)

    # word / def_groups / def_group [0] / gram_group[0]
    def test_first_gram_group_returns_3_children(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[0]

        with patch('src.html_to_json.SenseListGroup.build'):
            group = GramGroup(dict_parser, gram_group)
            group.build()
            result = group.translate()
            self.assertEqual({
                "value": "adjective",
                "defs": []}, result)

    def test_def_returns_def_json(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[0]
        sslist = dict_parser.get_senselist(gram_group)
        sslitem = dict_parser.get_all_senselist_items(sslist)[0]

        group = WordDefinition(dict_parser, sslitem)
        group.build()
        result = group.translate()
        self.assertEqual({
            "def": "characterized by, requiring, or capable of accuracy of detail; very accurate; methodical; correct",
            "example": "an exact science"}, result)

    def test_first_defs_returns_full_content(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[0]

        self.maxDiff = None

        group = SenseListGroup(dict_parser, gram_group)
        group.build()
        result = group.translate()
        self.assertEqual([
            {"def": "characterized by, requiring, or capable of accuracy of detail; very accurate; methodical; correct",
             "example": "an exact science"},
            {"def": "not deviating in form or content; without variation; precise", "example": "an exact replica"},
            {"def": "being the very (one specified or understood)", "example": "the exact spot where I put it"},
            {"def": "strict; severe; rigorous", "example": "an exact disciplinarian"}
        ], result)

    def test_first_gram_group_returns_full_content(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[0]

        group = GramGroup(dict_parser, gram_group)
        group.build()
        result = group.translate()

        self.assertEqual(
            {
                "value": "adjective",
                "defs": [
                    {"def": "characterized by, requiring, or capable of accuracy of detail; very accurate; methodical; correct",
                     "example": "an exact science"},
                    {"def": "not deviating in form or content; without variation; precise", "example": "an exact replica"},
                    {"def": "being the very (one specified or understood)", "example": "the exact spot where I put it"},
                    {"def": "strict; severe; rigorous", "example": "an exact disciplinarian"}
                ]
            }, result)

    def test_second_gram_group_returns_full_content(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[1]

        group = GramGroup(dict_parser, gram_group)
        group.build()
        result = group.translate()

        self.assertEqual(
            {
                "value": "transitive verb",
                "defs": [
                    {"def": "to force payment of; extort (with from or of)"},
                    {"def": "to demand and get by authority or force; insist on (with from or of)"},
                    {"def": "to call for; make necessary; require"}
                ]
            }, result)

    def test_first_def_group_returns_full_content(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]

        group = DefGroup(dict_parser, def_group)
        group.build()
        result = group.translate()
        self.assertEqual(
            {"word": "exact",
             "derived_forms": {"noun": "exactness, exactor exacter", "adjective": "exactable"},
             "gram_groups": [
                 {
                    "value": "adjective",
                    "defs": [
                        {"def": "characterized by, requiring, or capable of accuracy of detail; very accurate; methodical; correct",
                         "example": "an exact science"},
                        {"def": "not deviating in form or content; without variation; precise", "example": "an exact replica"},
                        {"def": "being the very (one specified or understood)", "example": "the exact spot where I put it"},
                        {"def": "strict; severe; rigorous", "example": "an exact disciplinarian"}
                    ]
                },
                {
                    "value": "transitive verb",
                    "defs": [
                        {"def": "to force payment of; extort (with from or of)"},
                        {"def": "to demand and get by authority or force; insist on (with from or of)"},
                        {"def": "to call for; make necessary; require"}
                    ]
                },
            ]}, result)

    def test_translate_def_groups(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)

        groups = DefGroups(dict_parser)
        groups.build()
        result = groups.translate()
        self.assertEqual(
            [
                {"word": "exact",
                 "derived_forms": {"noun": "exactness, exactor exacter", "adjective": "exactable"},
                 "gram_groups": [
                     {
                         "value": "adjective",
                         "defs": [
                             {"def": "characterized by, requiring, or capable of accuracy of detail; very accurate; methodical; correct",
                              "example": "an exact science"},
                             {"def": "not deviating in form or content; without variation; precise",
                              "example": "an exact replica"},
                             {"def": "being the very (one specified or understood)",
                              "example": "the exact spot where I put it"},
                             {"def": "strict; severe; rigorous", "example": "an exact disciplinarian"}
                         ]
                     },
                     {
                         "value": "transitive verb",
                         "defs": [
                             {"def": "to force payment of; extort (with from or of)"},
                             {"def": "to demand and get by authority or force; insist on (with from or of)"},
                             {"def": "to call for; make necessary; require"}
                         ]
                     },
                 ]}
            ], result)

    def test_word_returns_examples(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)

        group = ExamplesGroup(dict_parser)
        group.build()
        result = group.translate()
        self.assertEqual([
                {"example": "Her undershirt was tight enough that Savage could make out the exact lines of her body."}
            ], result)

    def test_word_returns_nearby_words(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)

        group = NearbyWordsGroup(dict_parser)
        group.build()
        result = group.translate()
        self.assertEqual([
            "ex nihilo", "ex officio", "ex parte", "ex post facto", "ex-", "ex-directory", "ex-dividend", "ex-voto",
            "exa-", "exacerbate", "exacta", "exacting", "exaction", "exactitude", "exactly", "exaggerate", "exalt",
            "exaltation", "exam", "examen"], result)

    def test_translate_html_to_json(self):
        obj = HtmlToJson(self.word_name, self.html_content)
        json_str = obj.translate()

        self.assertEqual(json_str,
        {
            "frequency": "Very Common",
            "def_groups": [
                {"word": "exact",
                 "derived_forms": {"noun": "exactness, exactor exacter", "adjective": "exactable"},
                 "gram_groups": [
                     {
                         "value": "adjective",
                         "defs": [
                             { "def": "characterized by, requiring, or capable of accuracy of detail; very accurate; methodical; correct",
                               "example": "an exact science"},
                             {"def": "not deviating in form or content; without variation; precise",
                              "example": "an exact replica"},
                             {"def": "being the very (one specified or understood)",
                              "example": "the exact spot where I put it"},
                             {"def": "strict; severe; rigorous", "example": "an exact disciplinarian"}
                         ]
                     },
                     {
                         "value": "transitive verb",
                         "defs": [
                             {"def": "to force payment of; extort (with from or of)"},
                             {"def": "to demand and get by authority or force; insist on (with from or of)"},
                             {"def": "to call for; make necessary; require"}
                         ]
                     },
                 ]}
            ],
            "examples": [
                {"example": "Her undershirt was tight enough that Savage could make out the exact lines of her body."}
            ],
            "nearby_words": [
                "ex nihilo", "ex officio", "ex parte", "ex post facto", "ex-", "ex-directory", "ex-dividend", "ex-voto",
                "exa-", "exacerbate", "exacta", "exacting", "exaction", "exactitude", "exactly", "exaggerate", "exalt",
                "exaltation", "exam", "examen"
            ],
            "translations": [
                "Exact means correct, accurate, and complete in every way.I don't remember the exact words.",
                "When someone exacts something, they demand and obtain it from another person, especially because they are "
                "in a superior or more powerful position. exacts, exacting, exacted --- Already he has exacted a written apology "
                "from the chairman of the commission."
            ]
        })

if __name__ == '__main__':
    unittest.main()
