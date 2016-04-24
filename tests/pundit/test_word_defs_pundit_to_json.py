import unittest
from unittest.mock import patch
from src.html_parser.def_groups import *
from src.html_parser.def_parser import DefParser
from lxml import etree


class HtmlToJsonTest(unittest.TestCase):

    def setUp(self):
        f = open("pundit_defs.html")
        self.word_name = "pundit"

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

        with patch.object(DefGroup, 'build') as mock:
            mock.return_value = None
            group = DefGroup(dict_parser, etree_group)
            group.build()
            result = group.translate()
            self.assertEqual({"word": "pundit", "gram_groups": []}, result)

    # word / def_groups
    def test_def_groups_returns_1_def_groups(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)

        with patch.object(DefGroup, 'build'):
            group = DefGroups(dict_parser)
            group.build()
            result = group.translate()
            self.assertEqual([{"word": "pundit", "gram_groups": []}],
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
                self.assertEqual({"word": "pundit", "derived_forms": {'noun': 'punditry'}, "gram_groups": [{}]},
                                 result)

    # word / def_groups / def_group [0] / gram_group[0]
    def test_first_gram_group_returns_1_child(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[0]

        with patch.object(SenseListGroup, 'build'):
            group = GramGroup(dict_parser, gram_group)
            group.build()
            result = group.translate()
            self.assertEqual({
                "value": "noun",
                "defs": []}, result)

    def test_defs_group_1_returns_2_empty_items(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[0]

        with patch.object(WordDefinition, 'build'):
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
        self.assertEqual({"category": "var. of", "def": "pandit (def. 1)"}, result)

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
            {"category": "var. of", "def": "pandit (def. 1)"},
            {"def": "a person who has or professes to have great learning; actual or self-professed authority"}
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
                "value": "noun",
                "defs": [
                    {"category": "var. of", "def": "pandit (def. 1)"},
                    {"def": "a person who has or professes to have great learning; actual or self-professed authority"}
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
            {"word": "pundit",
             "derived_forms": {'noun': 'punditry'},
             "gram_groups": [
                 {
                    "value": "noun",
                    "defs": [
                        {"category": "var. of", "def": "pandit (def. 1)"},
                        {"def": "a person who has or professes to have great learning; actual or self-professed authority"}
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
                {"word": "pundit",
                 "derived_forms": {'noun': 'punditry'},
                 "gram_groups": [
                     {
                         "value": "noun",
                         "defs": [
                             {"category": "var. of", "def": "pandit (def. 1)"},
                             {
                                 "def": "a person who has or professes to have great learning; actual or self-professed authority"}
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
                {"example": "Everyone who was anyone on the political pundit circuit had to have Amés appear on his or "
                 "her show or play in his or her game milieu."}
            ], result)

    def test_word_returns_nearby_words(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)

        group = NearbyWordsGroup(dict_parser)
        group.build()
        result = group.translate()
        self.assertEqual([
            "punctate", "punctilio", "punctilious", "punctual", "punctuate", "punctuated equilibrium", "punctuation",
            "punctuation mark", "punctulate", "puncture", "Pune", "pung", "pungent", "Punic", "Punic Wars", "puniness",
            "punish", "punishable", "punishment", "punitive"
        ], result)

    def test_get_translations_to_json(self):
        obj = HtmlToJson(self.word_name, self.html_content)
        json_obj = obj.translate()

        print(json_obj["translations"])
        self.assertEqual(json_obj["translations"],
            ["A pundit is a person who knows a lot about a subject and is often asked to give information or opinions "
             "about it to the public. pundits --- ...a well-known political pundit."])

    def test_translate_html_to_json(self):
        obj = HtmlToJson(self.word_name, self.html_content)
        json_str = obj.translate()

        self.assertEqual(json_str,
        {
            "frequency": "Used Occasionally",
            "def_groups": [
                {"word": "pundit",
                 "derived_forms": {'noun': 'punditry'},
                 "gram_groups": [
                     {
                         "value": "noun",
                         "defs": [
                             {"category": "var. of", "def": "pandit (def. 1)"},
                             {"def": "a person who has or professes to have great learning; actual or self-professed authority"}
                         ]
                     }
                 ]}
            ],
            "examples": [
                {"example": "Everyone who was anyone on the political pundit circuit had to have Amés appear on his or "
                            "her show or play in his or her game milieu."}
            ],
            "nearby_words": [
                "punctate", "punctilio", "punctilious", "punctual", "punctuate", "punctuated equilibrium", "punctuation",
                "punctuation mark", "punctulate", "puncture", "Pune", "pung", "pungent", "Punic", "Punic Wars", "puniness",
                "punish", "punishable", "punishment", "punitive"
            ],
            "translations": [
                "A pundit is a person who knows a lot about a subject and is often asked to give information or opinions "
                "about it to the public. pundits --- ...a well-known political pundit."]
        })

if __name__ == '__main__':
    unittest.main()
