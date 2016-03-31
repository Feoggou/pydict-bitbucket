import unittest
from unittest.mock import patch
from src.def_groups import *
from src.def_parser import DefParser
from lxml import etree


class HtmlToJsonTest(unittest.TestCase):

    def setUp(self):
        f = open("affluent_defs.html")
        self.word_name = "affluent"

        self.html_content = f.read()
        # self.maxDiff = None

    def test_create_html_to_json_obj(self):
        obj = HtmlToJson(self.word_name, self.html_content)
        self.assertIsNotNone(obj)

    def test_word_freq_group_value_is_extremely_common(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)

        group = WordFrequencyGroup(dict_parser)
        group.build()
        result = group.translate()
        self.assertEqual(result, "In Common Usage")

    # word / def_groups
    def test_def_groups_returns_1_def_groups(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)

        with patch('src.def_groups.DefGroup.build'):
            group = DefGroups(dict_parser)
            group.build()
            result = group.translate()
            self.assertEqual([{"word": "affluent", "gram_groups": []}], result)

    # word / def_groups / def_group [0] / gram_groups
    def test_first_def_group_returns_2_gram_groups(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]

        with patch('src.def_groups.GramGroup.build'):
            with patch('src.def_groups.RelatedGroup.build'):
                group = DefGroup(dict_parser, def_group)
                group.build()
                result = group.translate()
                self.assertEqual({"word": "affluent",
                                  'derived_forms': {'adverb': 'affluently'},
                                  "gram_groups": [{}, {}]}, result)

    # word / def_groups / def_group [0] / gram_group[0]
    def test_first_gram_group_returns_simple(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[0]

        with patch('src.def_groups.SenseListGroup.build'):
            group = GramGroup(dict_parser, gram_group)
            group.build()
            result = group.translate()
            self.assertEqual({
                "value": "adjective",
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
        self.assertEqual({"def": "flowing freely"}, result)

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
            {"def": "flowing freely"},
            {"def": "plentiful; abundant"},
            {"def": "wealthy; prosperous; rich", "example": "the affluent society"}
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
                "value": "adjective",
                "defs": [
                    {"def": "flowing freely"},
                    {"def": "plentiful; abundant"},
                    {"def": "wealthy; prosperous; rich", "example": "the affluent society"}
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
                    {"def": "a tributary stream opposed to effluent (def. 1)noun, effluent (sense 2a) (def. 1)"},
                    {"def": "an affluent person"}
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
            {"word": "affluent",
             'derived_forms': {'adverb': 'affluently'},
             "gram_groups": [
                 {
                     "value": "adjective",
                     "defs": [
                         {"def": "flowing freely"},
                         {"def": "plentiful; abundant"},
                         {"def": "wealthy; prosperous; rich", "example": "the affluent society"}
                     ]
                },
                {
                    "value": "noun",
                    "defs": [
                        {"def": "a tributary stream opposed to effluent (def. 1)noun, effluent (sense 2a) (def. 1)"},
                        {"def": "an affluent person"}
                    ]
                },
            ]}, result)

    def test_translate_def_groups(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)

        groups = DefGroups(dict_parser)
        groups.build()
        result = groups.translate()
        self.assertEqual(
            [
                {"word": "affluent",
                 'derived_forms': {'adverb': 'affluently'},
                 "gram_groups": [
                     {
                         "value": "adjective",
                         "defs": [
                             {"def": "flowing freely"},
                             {"def": "plentiful; abundant"},
                             {"def": "wealthy; prosperous; rich", "example": "the affluent society"}
                         ]
                     },
                     {
                         "value": "noun",
                         "defs": [
                             {
                                 "def": "a tributary stream opposed to effluent (def. 1)noun, effluent (sense 2a) (def. 1)"},
                             {"def": "an affluent person"}
                         ]
                     },
                 ]}
            ], result)

    def test_word_returns_examples(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)

        group = ExamplesGroup(dict_parser)
        group.build()
        result = group.translate()
        self.assertEqual([
                {"example": "Adam Berendt who'd lived so frugally in the midst of affluent Salthill."}
            ], result)

    def test_word_returns_nearby_words(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)

        group = NearbyWordsGroup(dict_parser)
        group.build()
        result = group.translate()
        self.assertEqual([
            "affirmative", "affirmative action", "affix", "affixation", "affixture", "afflatus", "afflict", "affliction",
            "afflictive", "affluence", "afflux", "afford", "afforest", "affranchise", "affray", "affricate",
            "affrication", "affright", "affront", "affusion"], result)

    def test_get_translations_to_json(self):
        obj = HtmlToJson(self.word_name, self.html_content)
        json_obj = obj.translate()

        self.assertEqual(json_obj["translations"],
            ["If you are affluent, you have a lot of money.It is one of the most affluent areas in the country.",
             "The affluent are people who are affluent.The diet of the affluent has not changed much over the decades."])

    def test_translate_html_to_json(self):
        obj = HtmlToJson(self.word_name, self.html_content)
        json_str = obj.translate()

        self.assertEqual(json_str,
        {
            "frequency": "In Common Usage",
            "def_groups": [
                {"word": "affluent",
                 'derived_forms': {'adverb': 'affluently'},
                 "gram_groups": [
                     {
                         "value": "adjective",
                         "defs": [
                             {"def": "flowing freely"},
                             {"def": "plentiful; abundant"},
                             {"def": "wealthy; prosperous; rich", "example": "the affluent society"}
                         ]
                     },
                     {
                         "value": "noun",
                         "defs": [
                             {
                                 "def": "a tributary stream opposed to effluent (def. 1)noun, effluent (sense 2a) (def. 1)"},
                             {"def": "an affluent person"}
                         ]
                     },
                 ]}
            ],
            "examples": [
                {"example": "Adam Berendt who'd lived so frugally in the midst of affluent Salthill."}
            ],
            "nearby_words": [
                "affirmative", "affirmative action", "affix", "affixation", "affixture", "afflatus", "afflict", "affliction",
                "afflictive", "affluence", "afflux", "afford", "afforest", "affranchise", "affray", "affricate",
                "affrication", "affright", "affront", "affusion"
            ],
            "translations": [
                "If you are affluent, you have a lot of money.It is one of the most affluent areas in the country.",
                "The affluent are people who are affluent.The diet of the affluent has not changed much over the decades."
            ]
        })

if __name__ == '__main__':
    unittest.main()
