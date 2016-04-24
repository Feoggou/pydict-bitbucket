import unittest
from unittest.mock import patch
from src.html_parser.def_groups import *
from src.html_parser.def_parser import DefParser
from lxml import etree


class HtmlToJsonTest(unittest.TestCase):

    def setUp(self):
        f = open("pell-mell_defs.html")
        self.word_name = "pell-mell"

        self.html_content = f.read()
        # self.maxDiff = None

    # word / def_groups / def_group [0]
    def test_first_def_group_returns_no_items(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        etree_group = dict_parser.get_all_def_groups()[0]

        with patch.object(DefGroup, 'build') as mock:
            mock.return_value = None
            group = DefGroup(dict_parser, etree_group)
            group.build()
            result = group.translate()
            self.assertEqual({"word": "pell-mell", "gram_groups": []}, result)

    # word / def_groups
    def test_def_groups_returns_1_def_groups(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)

        with patch.object(DefGroup, 'build'):
            group = DefGroups(dict_parser)
            group.build()
            result = group.translate()
            self.assertEqual([{"word": "pell-mell", "gram_groups": []}],
                result)

    # word / def_groups / def_group [0] / gram_groups
    def test_first_def_group_returns_4_gram_groups(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]

        with patch.object(GramGroup, 'build'):
            with patch.object(RelatedGroup, 'build'):
                group = DefGroup(dict_parser, def_group)
                group.build()
                result = group.translate()
                self.assertEqual({"word": "pell-mell", "gram_groups": [{}, {}]},
                                 result)

    # word / def_groups / def_group [0] / gram_group[0]
    def test_first_gram_group_returns_gram_value(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[0]

        with patch.object(SenseListGroup, 'build'):
            group = GramGroup(dict_parser, gram_group)
            group.build()
            result = group.translate()
            self.assertEqual({
                "value": "adverb adjective",
                "defs": []}, result)

    def test_def_returns_def_json(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[0]
        sslist = dict_parser.get_senselist(gram_group)
        sslitem = dict_parser.get_all_senselist_items(sslist)[0]

        group = WordDefinition(dict_parser, sslitem)
        group.build()
        result = group.translate()
        self.assertEqual({"def": "in a jumbled, confused mass or manner; without order or method"}, result)

    def test_first_defs_returns_full_content(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[0]

        self.maxDiff = None

        group = SenseListGroup(dict_parser, gram_group)
        group.build()
        result = group.translate()
        self.assertEqual([
            {"def": "in a jumbled, confused mass or manner; without order or method"},
            {"def": "in wild, disorderly haste; headlong"}
        ], result)

    def test_first_gram_group_returns_full_content(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[0]

        group = GramGroup(dict_parser, gram_group)
        group.build()
        result = group.translate()

        self.assertEqual(
            {
                "value": "adverb adjective",
                "defs": [
                    {"def": "in a jumbled, confused mass or manner; without order or method"},
                    {"def": "in wild, disorderly haste; headlong"}
                ]
            }, result)

    def test_second_gram_group_returns_full_content(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[1]

        group = GramGroup(dict_parser, gram_group)
        group.build()
        result = group.translate()

        self.assertEqual(
            {
                "value": "noun",
                "defs": [
                    {"def": "a jumble; confusion; disorder"}
                ]
            }, result)

    def test_first_def_group_returns_full_content(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]

        group = DefGroup(dict_parser, def_group)
        group.build()
        result = group.translate()
        self.assertEqual(
            {"word": "pell-mell",
             "gram_groups": [
                 {
                    "value": "adverb adjective",
                    "defs": [
                        {"def": "in a jumbled, confused mass or manner; without order or method"},
                        {"def": "in wild, disorderly haste; headlong"}
                    ]
                },
                {
                    "value": "noun",
                    "defs": [
                        {"def": "a jumble; confusion; disorder"}
                    ]
                }
            ]}, result)

    def test_translate_def_groups(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)

        groups = DefGroups(dict_parser)
        groups.build()
        result = groups.translate()
        self.assertEqual(
            [
                {"word": "pell-mell",
                 "gram_groups": [
                     {
                         "value": "adverb adjective",
                         "defs": [
                             {"def": "in a jumbled, confused mass or manner; without order or method"},
                             {"def": "in wild, disorderly haste; headlong"}
                         ]
                     },
                     {
                         "value": "noun",
                         "defs": [
                             {"def": "a jumble; confusion; disorder"}
                         ]
                     }
                 ]}
            ], result)

    def test_word_returns_examples(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)

        group = ExamplesGroup(dict_parser)
        group.build()
        result = group.translate()
        self.assertEqual([
                {"example": "Somehow in his pell-mell race through the woods he had left her behind."}
            ], result)

    def test_word_returns_nearby_words(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)

        group = NearbyWordsGroup(dict_parser)
        group.build()
        result = group.translate()
        self.assertEqual([
            "pelecypod", "Pelée", "pelerine", "Peleus", "pelf", "Pelias", "pelican", "pelican hook", "Pelion", "pelisse",
            "pellagra", "pellagrin", "pellet", "pelletize", "pellicle", "pellitory", "pellucid", "pelmet", "Pelopidas",
            "Peloponnesian War"
        ], result)

    def test_get_translations_to_json(self):
        obj = HtmlToJson(self.word_name, self.html_content)
        json_obj = obj.translate()

        self.assertEqual(json_obj["translations"], [])

    def test_translate_html_to_json(self):
        obj = HtmlToJson(self.word_name, self.html_content)
        json_str = obj.translate()

        self.assertEqual(json_str,
        {
            "frequency": "",
            "def_groups": [
                {"word": "pell-mell",
                 "gram_groups": [
                     {
                         "value": "adverb adjective",
                         "defs": [
                             {"def": "in a jumbled, confused mass or manner; without order or method"},
                             {"def": "in wild, disorderly haste; headlong"}
                         ]
                     },
                     {
                         "value": "noun",
                         "defs": [
                             {"def": "a jumble; confusion; disorder"}
                         ]
                     }
                 ]}
            ],
            "examples": [
                {"example": "Somehow in his pell-mell race through the woods he had left her behind."}
            ],
            "nearby_words": [
                "pelecypod", "Pelée", "pelerine", "Peleus", "pelf", "Pelias", "pelican", "pelican hook", "Pelion", "pelisse",
                "pellagra", "pellagrin", "pellet", "pelletize", "pellicle", "pellitory", "pellucid", "pelmet", "Pelopidas",
                "Peloponnesian War"
            ],
            "translations": []
        })

if __name__ == '__main__':
    unittest.main()
