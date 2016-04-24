import unittest
from unittest.mock import patch
from src.html_parser.def_groups import *
from src.html_parser.def_parser import DefParser
from lxml import etree


class HtmlToJsonTest(unittest.TestCase):

    def setUp(self):
        f = open("un-_defs.html")
        self.word_name = "un-"

        self.html_content = f.read()
        # self.maxDiff = None

    def test_create_html_to_json_obj(self):
        obj = HtmlToJson(self.word_name, self.html_content)
        self.assertIsNotNone(obj)

    # word / def_groups
    def test_def_groups_returns_1_def_groups(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)

        with patch.object(DefGroup, 'build'):
            group = DefGroups(dict_parser)
            group.build()
            result = group.translate()
            print(result)
            self.assertEqual([{"word": "un-", "gram_groups": []}], result)

    # word / def_groups / def_group [0] / gram_groups
    def test_first_def_group_returns_1_gram_groups(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]

        with patch.object(GramGroup, 'build'):
            with patch.object(RelatedGroup, 'build'):
                group = DefGroup(dict_parser, def_group)
                group.build()
                result = group.translate()
                self.assertEqual(
                    {"word": "un-",
                     'semantics': 'The following list includes many of the more common compounds formed with un- '
                                  '(either sense) that do not have special meanings ',
                     "gram_groups": [{}]}, result)

    # word / def_groups / def_group [0] / gram_group[0]
    def test_first_gram_group_returns_content(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[0]

        with patch.object(SenseListGroup, 'build'):
            group = GramGroup(dict_parser, gram_group)
            group.build()
            result = group.translate()
            self.assertEqual({
                "defs": []}, result)

    def test_first_def_returns_def_json(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[0]
        sslist = dict_parser.get_senselist(gram_group)
        sslitem = dict_parser.get_all_senselist_items(sslist)[0]

        group = WordDefinition(dict_parser, sslitem)
        group.build()
        result = group.translate()
        self.assertEqual({"def": "not, lack of, the opposite of see also non- (def. 1)", "example": "unconcern, unreason, unwonted"}, result)

    def test_second_def_returns_def_json(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[0]
        sslist = dict_parser.get_senselist(gram_group)
        sslitem = dict_parser.get_all_senselist_items(sslist)[1]

        group = WordDefinition(dict_parser, sslitem)
        group.build()
        result = group.translate()
        self.assertEqual(
            {"def": "back; the reverse or removal of (added to verbs to indicate a reversal of the action and to nouns "
             "to indicate a removal or release of the thing mentioned or from the condition, place, etc. indicated, and "
             "sometimes used merely as an intensive [unbind, unfold; unbonnet, unbosom; unloose])"},
            result)

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
            {"def": "not, lack of, the opposite of see also non- (def. 1)", "example": "unconcern, unreason, unwonted"},
            {"def": "back; the reverse or removal of (added to verbs to indicate a reversal of the action and to nouns "
                    "to indicate a removal or release of the thing mentioned or from the condition, place, etc. indicated, and "
                    "sometimes used merely as an intensive [unbind, unfold; unbonnet, unbosom; unloose])"}
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
                "defs": [
                    {"def": "not, lack of, the opposite of see also non- (def. 1)",
                     "example": "unconcern, unreason, unwonted"},
                    {"def": "back; the reverse or removal of (added to verbs to indicate a reversal of the action and to nouns "
                     "to indicate a removal or release of the thing mentioned or from the condition, place, etc. indicated, and "
                     "sometimes used merely as an intensive [unbind, unfold; unbonnet, unbosom; unloose])"}
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
            {"word": "un-",
             'semantics': 'The following list includes many of the more common compounds formed with un- '
                          '(either sense) that do not have special meanings ',
             "gram_groups": [
                 {
                     "defs": [
                         {"def": "not, lack of, the opposite of see also non- (def. 1)",
                          "example": "unconcern, unreason, unwonted"},
                         {
                             "def": "back; the reverse or removal of (added to verbs to indicate a reversal of the action and to nouns "
                                    "to indicate a removal or release of the thing mentioned or from the condition, place, etc. indicated, and "
                                    "sometimes used merely as an intensive [unbind, unfold; unbonnet, unbosom; unloose])"}
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
                {"word": "un-",
                 'semantics': 'The following list includes many of the more common compounds formed with un- '
                              '(either sense) that do not have special meanings ',
                 "gram_groups": [
                     {
                         "defs": [
                             {"def": "not, lack of, the opposite of see also non- (def. 1)",
                              "example": "unconcern, unreason, unwonted"},
                             {
                                 "def": "back; the reverse or removal of (added to verbs to indicate a reversal of the action and to nouns "
                                        "to indicate a removal or release of the thing mentioned or from the condition, place, etc. indicated, and "
                                        "sometimes used merely as an intensive [unbind, unfold; unbonnet, unbosom; unloose])"}
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
                {"example": "The panic slowly subsided to un- easy apprehension while the minutes crawled by as if they were each an hour long."}
            ], result)

    def test_word_returns_nearby_words(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)

        group = NearbyWordsGroup(dict_parser)
        group.build()
        result = group.translate()
        self.assertEqual([
            "Umbundu", "umiak", "umlaut", "ump", "umpirage", "umpire", "umpteen", "Umtata", "UMW", "UN", "un-American",
            "Una", "una corda", "unabashed", "unable", "unabridged", "unaccommodated", "unaccompanied", "unaccomplished",
            "unaccountable"
        ], result)

    def test_translate_html_to_json(self):
        obj = HtmlToJson(self.word_name, self.html_content)
        json_str = obj.translate()

        self.assertEqual(json_str,
        {
            "frequency": '',
            "def_groups": [
                {"word": "un-",
                 'semantics': 'The following list includes many of the more common compounds formed with un- '
                              '(either sense) that do not have special meanings ',
                 "gram_groups": [
                     {
                         "defs": [
                             {"def": "not, lack of, the opposite of see also non- (def. 1)",
                              "example": "unconcern, unreason, unwonted"},
                             {
                                 "def": "back; the reverse or removal of (added to verbs to indicate a reversal of the action and to nouns "
                                        "to indicate a removal or release of the thing mentioned or from the condition, place, etc. indicated, and "
                                        "sometimes used merely as an intensive [unbind, unfold; unbonnet, unbosom; unloose])"}
                         ]
                     }
                 ]}
            ],
            "examples": [
                {"example": "The panic slowly subsided to un- easy apprehension while the minutes crawled by as if they were each an hour long."}
            ],
            "nearby_words": [
                "Umbundu", "umiak", "umlaut", "ump", "umpirage", "umpire", "umpteen", "Umtata", "UMW", "UN", "un-American",
                "Una", "una corda", "unabashed", "unable", "unabridged", "unaccommodated", "unaccompanied", "unaccomplished",
                "unaccountable"
            ],
            "translations": []
        })

if __name__ == '__main__':
    unittest.main()
