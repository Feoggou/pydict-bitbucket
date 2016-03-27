import unittest
from unittest.mock import patch
from src.def_groups import *
from src.def_parser import DefParser
from src.html_to_json import HtmlToJson
from lxml import etree


class HtmlToJsonTest(unittest.TestCase):

    def setUp(self):
        f = open("bellow_defs.html")
        self.word_name = "bellow"

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
        self.assertEqual(result, "Used Occasionally")


    # word / def_groups / def_group [0]
    def test_first_def_group_returns_no_items(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        etree_group = dict_parser.get_all_def_groups()[0]

        with patch('src.html_to_json.DefGroup.build') as mock:
            mock.return_value = None
            group = DefGroup(dict_parser, etree_group)
            group.build()
            result = group.translate()
            self.assertEqual({"word": "bellow", "gram_groups": []}, result)

    # word / def_groups
    def test_def_groups_returns_2_def_groups(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)

        with patch('src.html_to_json.DefGroup.build'):
            group = DefGroups(dict_parser)
            group.build()
            result = group.translate()
            self.assertEqual([{"word": "bellow", "gram_groups": []},
                              {"word": "Bellow", "gram_groups": []}],
                result)

    # word / def_groups / def_group [0] / gram_groups
    def test_first_def_group_returns_3_gram_groups(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]

        with patch('src.html_to_json.GramGroup.build'):
            with patch('src.html_to_json.RelatedGroup.build'):
                group = DefGroup(dict_parser, def_group)
                group.build()
                result = group.translate()
                self.assertEqual({"word": "bellow", "gram_groups": [{}, {}, {}]},
                                 result)

    # word / def_groups / def_group [0] / gram_group[0]
    def test_first_gram_group_returns_gram_value(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[0]

        with patch('src.html_to_json.SenseListGroup.build'):
            group = GramGroup(dict_parser, gram_group)
            group.build()
            result = group.translate()
            self.assertEqual({
                "value": "intransitive verb",
                "defs": []}, result)

    def test_defs_group_1_returns_2_empty_items(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[0]

        with patch('src.html_to_json.WordDefinition.build'):
            group = SenseListGroup(dict_parser, gram_group)
            group.build()
            result = group.translate()
            self.assertEqual([{"def": ""}, {"def": ""}], result)

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
        self.assertEqual({"def": "to roar with a powerful, reverberating sound, as a bull does"}, result)

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
            {"def": "to roar with a powerful, reverberating sound, as a bull does"},
            {"def": "to cry out loudly, as in anger or pain"}
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
                "value": "intransitive verb",
                "defs": [
                    {"def": "to roar with a powerful, reverberating sound, as a bull does"},
                    {"def": "to cry out loudly, as in anger or pain"}
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
                "value": "transitive verb",
                "defs": [
                    {"def": "to utter loudly or powerfully"}
                ]
            }, result)

    def test_third_gram_group_returns_full_content(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[2]

        group = GramGroup(dict_parser, gram_group)
        group.build()
        result = group.translate()

        self.assertEqual(
            {
                "value": "noun",
                "defs": [
                    {"def": "the sound of bellowing"},
                ]
            }, result)

    def test_2nd_defs_group_gram_group_returns_full_content(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[1]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[0]

        group = GramGroup(dict_parser, gram_group)
        group.build()
        result = group.translate()
        print("result=", result)

        self.assertEqual(
            {
                "defs": [
                    {'def': 'Saul(born Solomon Bellows) 1915-2005; U.S. novelist, born in Canada'},
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
            {"word": "bellow",
             "gram_groups": [
                 {
                    "value": "intransitive verb",
                    "defs": [
                        {"def": "to roar with a powerful, reverberating sound, as a bull does"},
                        {"def": "to cry out loudly, as in anger or pain"}
                    ]
                },
                {
                    "value": "transitive verb",
                    "defs": [
                        {"def": "to utter loudly or powerfully"}
                    ]
                },
                {
                    "value": "noun",
                    "defs": [
                        {"def": "the sound of bellowing"},
                    ]
                },
            ]}, result)

    def test_second_def_group_returns_full_content(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[1]

        group = DefGroup(dict_parser, def_group)
        group.build()
        result = group.translate()
        self.assertEqual(
            {"word": "Bellow", "gram_groups": [
                {
                    "defs": [
                        {'def': 'Saul(born Solomon Bellows) 1915-2005; U.S. novelist, born in Canada'},
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
                {"word": "bellow",
                 "gram_groups": [
                     {
                         "value": "intransitive verb",
                         "defs": [
                             {"def": "to roar with a powerful, reverberating sound, as a bull does"},
                             {"def": "to cry out loudly, as in anger or pain"}
                         ]
                     },
                     {
                         "value": "transitive verb",
                         "defs": [
                             {"def": "to utter loudly or powerfully"}
                         ]
                     },
                     {
                         "value": "noun",
                         "defs": [
                             {"def": "the sound of bellowing"},
                         ]
                     },
                 ]},
                {"word": "Bellow", "gram_groups": [
                    {
                        "defs": [
                            {'def': 'Saul(born Solomon Bellows) 1915-2005; U.S. novelist, born in Canada'},
                        ]
                    },
                ]}
            ], result)

    def test_word_returns_nearby_words(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)

        group = NearbyWordsGroup(dict_parser)
        group.build()
        result = group.translate()
        self.assertEqual([
            "belligerence", "belligerency", "belligerent", "Bellingham", "Bellingshausen Sea", "Bellini", "bellman",
            "bellmouthed", "Belloc", "Bellona", "bellows", "bells and whistles", "bellwether", "bellwort", "belly",
            "belly dance", "belly laugh", "belly up", "belly-flop", "bellyache"], result)

    def test_get_translations_to_json(self):
        obj = HtmlToJson(self.word_name, self.html_content)
        json_obj = obj.translate()

        self.assertEqual(json_obj["translations"],
            ["If someone bellows, they shout angrily in a loud, deep voice. bellowed, bellowing, bellows --- I didn't "
             "ask to be born! she bellowed.I could hear the crowd bellowing."])

    def test_translate_html_to_json(self):
        obj = HtmlToJson(self.word_name, self.html_content)
        json_str = obj.translate()

        self.assertEqual(json_str,
        {
            "frequency": "Used Occasionally",
            "def_groups": [
                {"word": "bellow",
                 "gram_groups": [
                     {
                         "value": "intransitive verb",
                         "defs": [
                             {"def": "to roar with a powerful, reverberating sound, as a bull does"},
                             {"def": "to cry out loudly, as in anger or pain"}
                         ]
                     },
                     {
                         "value": "transitive verb",
                         "defs": [
                             {"def": "to utter loudly or powerfully"}
                         ]
                     },
                     {
                         "value": "noun",
                         "defs": [
                             {"def": "the sound of bellowing"},
                         ]
                     },
                 ]},
                {"word": "Bellow", "gram_groups": [
                    {
                        "defs": [
                            {'def': 'Saul(born Solomon Bellows) 1915-2005; U.S. novelist, born in Canada'},
                        ]
                    },
                ]}
            ],
            "examples": [],
            "nearby_words": [
                "belligerence", "belligerency", "belligerent", "Bellingham", "Bellingshausen Sea", "Bellini", "bellman",
                "bellmouthed", "Belloc", "Bellona", "bellows", "bells and whistles", "bellwether", "bellwort", "belly",
                "belly dance", "belly laugh", "belly up", "belly-flop", "bellyache"
            ],
            "translations": [
                "If someone bellows, they shout angrily in a loud, deep voice. bellowed, bellowing, bellows --- I didn't "
                "ask to be born! she bellowed.I could hear the crowd bellowing."
            ]
        })

if __name__ == '__main__':
    unittest.main()
