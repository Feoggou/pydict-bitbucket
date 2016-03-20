import unittest
from unittest.mock import patch
from def_groups import *
from dict_parse import DictParser
import html_to_json
from html_to_json import HtmlToJson
from lxml import etree


class HtmlToJsonTest(unittest.TestCase):

    def setUp(self):
        f = open("do_defs.html")
        self.word_name = "do"

        self.html_content = f.read()
        # self.maxDiff = None

    def test_create_html_to_json_obj(self):
        obj = HtmlToJson(self.word_name, self.html_content)
        self.assertIsNotNone(obj)

    def test_translate_empty_main_to_json_returns_empty_word(self):
        obj = HtmlToJson(self.word_name, self.html_content)

        with patch('html_to_json.MainDefGroup.build_children') as mock:
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
        self.assertEqual(result, "Extremely Common")

    # word / def_groups
    def test_def_groups_returns_empty_groups(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)

        with patch('html_to_json.DefGroups.build') as mock:
            group = DefGroups(dict_parser)
            group.build()
            result = group.translate()
            self.assertEqual([], result)

    # word / def_groups / def_group [0]
    def test_first_def_group_returns_no_items(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)
        etree_group = dict_parser.get_all_def_groups()[0]

        with patch('html_to_json.DefGroup.build') as mock:
            mock.return_value = None
            group = DefGroup(dict_parser, etree_group)
            group.build()
            result = group.translate()
            self.assertEqual({"word": "do", "gram_groups": []}, result)

    # word / def_groups
    def test_def_groups_returns_5_def_groups(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)

        with patch('html_to_json.DefGroup.build'):
            group = DefGroups(dict_parser)
            group.build()
            result = group.translate()
            self.assertEqual([
                {"word": "do", "gram_groups": []}, {"word": "do", "gram_groups": []},
                {"word": "do", "gram_groups": []}, {"word": "Do or do", "gram_groups": []},
                {"word": "DO or D.O.", "gram_groups": []}],
                result)

    # word / def_groups / def_group [0] / gram_groups
    def test_first_def_group_returns_4_gram_groups(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]

        with patch('html_to_json.GramGroup.build'):
            with patch('html_to_json.RelatedGroup.build'):
                group = DefGroup(dict_parser, def_group)
                group.build()
                result = group.translate()
                self.assertEqual({"word": "do", "gram_groups": [{}, {}, {}, {}]},
                                 result)

    # word / def_groups / def_group [0] / gram_group[0]
    def test_first_gram_group_returns_3_children(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[0]

        with patch('html_to_json.SenseListGroup.build'):
            group = GramGroup(dict_parser, gram_group)
            group.build()
            result = group.translate()
            self.assertEqual({
                "word_forms": ["did", "done", "doing"],
                "value": "transitive verb",
                "defs": []}, result)

    def test_empty_defs_returns_empty(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[0]

        with patch('html_to_json.SenseListGroup.build'):
            group = SenseListGroup(dict_parser, gram_group)
            group.build()
            result = group.translate()
            self.assertEqual([], result)

    def test_defs_group_3_returns_3_empty_items(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[3]

        with patch('html_to_json.WordDefinition.build'):
            group = SenseListGroup(dict_parser, gram_group)
            group.build()
            result = group.translate()
            self.assertEqual([{"def": ""}, {"def": ""}, {"def": ""}], result)

    def test_def_returns_def_json(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[3]
        sslist = dict_parser.get_senselist(gram_group)
        sslitem = dict_parser.get_all_senselist_items(sslist)[2]

        group = WordDefinition(dict_parser, sslitem)
        group.build()
        result = group.translate()
        self.assertEqual({"category": "slang", "def": "excrement; feces", "example": "dog do"}, result)

    def test_def_subgroup_returns_full_defs(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[0]
        sslist = dict_parser.get_senselist(gram_group)
        sslitem = dict_parser.get_all_senselist_items(sslist)[0]

        group = WordDefinition(dict_parser, sslitem)
        group.build()
        result = group.translate()
        self.assertEqual({"def_subgroup": [
            {"def": "to execute; effect; perform (an act, action, etc.)", "example": "do great deeds"},
            {"def": "to carry out; fulfill", "example": "do what I tell you"}
        ]}, result)

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
            {"def_subgroup": [
                {"def": "to execute; effect; perform (an act, action, etc.)", "example": "do great deeds"},
                {"def": "to carry out; fulfill", "example": "do what I tell you"}
            ]},
            {"def": "to bring to completion; finish", "example": "dinner has been done for an hour"},
            {"def": "to bring about; cause; produce", "example": "it does no harm; who did this to you?"},
            {"def": "to exert (efforts, etc.)", "example": "do your best"},
            {"def": "to have or take (a meal)", "example": "let\'s do lunch"},
            {"def": "to deal with as is required; attend to", "example": "do the ironing, do one\'s nails or hair"},
            {"def": "to have as one\'s work or occupation; work at or on", "example": "what does he do for a living?"},
            {"def": "to work out; solve", "example": "do a problem"},
            {"def": "to produce or appear in (a play, etc.)", "example": "we did Hamlet"},
            {"def_subgroup": [
                {"def": "to play the role of", "example": "I did Polonius"},
                {"category": "informal", "def": "to imitate, or behave characteristically as", "example": "to do a Houdini"},
            ]},
            {"def": "to write or publish (a book), compose (a musical score), etc."},
            {"def_subgroup": [
                {"def": "to cover (distance)", "example": "to do a mile in four minutes"},
                {"def": "to move along at a speed of", "example": "to do 60 miles an hour"},
            ]},
            {"def": "to visit as a sightseer; tour", "example": "they did England in two months"},
            {"def": "to translate", "example": "to do Horace into English"},
            {"def": "to give; render", "example": "to do honor to the dead"},
            {"def": "to suit; be convenient to", "example": "this will do me very well"},
            {"category": "informal", "def_subgroup": [
                {"def": "to prepare; cook", "example": "that restaurant does ribs really well"},
                {"def": "to eat", "example": "let\'s do Mexican tonight"},
            ]},
            {"category": "informal", "def": "to cheat; swindle", "example": "you\'ve been done"},
            {"category": "informal", "def": "to serve (a jail term)"},
            {"category": "slang", "def": "to take; ingest; use", "example": "we\'ve never done drugs"},
            {"category": "slang", "def": "to perform a sexual act upon; specif., to have sexual intercourse with"},
            {"category": "slang", "def": "to kill"},
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
                "word_forms": ["did", "done", "doing"],
                "value": "transitive verb",
                "defs": [
                    {"def_subgroup": [
                        {"def": "to execute; effect; perform (an act, action, etc.)", "example": "do great deeds"},
                        {"def": "to carry out; fulfill", "example": "do what I tell you"}
                    ]},
                    {"def": "to bring to completion; finish", "example": "dinner has been done for an hour"},
                    {"def": "to bring about; cause; produce", "example": "it does no harm; who did this to you?"},
                    {"def": "to exert (efforts, etc.)", "example": "do your best"},
                    {"def": "to have or take (a meal)", "example": "let\'s do lunch"},
                    {"def": "to deal with as is required; attend to", "example": "do the ironing, do one\'s nails or hair"},
                    {"def": "to have as one\'s work or occupation; work at or on", "example": "what does he do for a living?"},
                    {"def": "to work out; solve", "example": "do a problem"},
                    {"def": "to produce or appear in (a play, etc.)", "example": "we did Hamlet"},
                    {"def_subgroup": [
                        {"def": "to play the role of", "example": "I did Polonius"},
                        {"category": "informal", "def": "to imitate, or behave characteristically as", "example": "to do a Houdini"},
                    ]},
                    {"def": "to write or publish (a book), compose (a musical score), etc."},
                    {"def_subgroup": [
                        {"def": "to cover (distance)", "example": "to do a mile in four minutes"},
                        {"def": "to move along at a speed of", "example": "to do 60 miles an hour"},
                    ]},
                    {"def": "to visit as a sightseer; tour", "example": "they did England in two months"},
                    {"def": "to translate", "example": "to do Horace into English"},
                    {"def": "to give; render", "example": "to do honor to the dead"},
                    {"def": "to suit; be convenient to", "example": "this will do me very well"},
                    {"category": "informal", "def_subgroup": [
                        {"def": "to prepare; cook", "example": "that restaurant does ribs really well"},
                        {"def": "to eat", "example": "let\'s do Mexican tonight"},
                    ]},
                    {"category": "informal", "def": "to cheat; swindle", "example": "you\'ve been done"},
                    {"category": "informal", "def": "to serve (a jail term)"},
                    {"category": "slang", "def": "to take; ingest; use", "example": "we\'ve never done drugs"},
                    {"category": "slang", "def": "to perform a sexual act upon; specif., to have sexual intercourse with"},
                    {"category": "slang", "def": "to kill"},
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
                "value": "intransitive verb",
                "defs": [
                    {"def": "to act in a specified way; behave", "example": "he does well when treated well"},
                    {"def": "to be active; work", "example": "do; don\'t merely talk"},
                    {"def": "to finish", "category": "used in the perfect tense [have done with dreaming ]"},
                    {"def": "to get along; fare", "example": "mother and child are doing well"},
                    {"def": "to be adequate or suitable; serve the purpose", "example": "the black dress will do"},
                    {"def": "to take place; go on", "example": "anything doing tonight?"},
                    {"category": "mainly British, informal", "def": "used as a substitute verb after a modal auxiliary or a form of have in a perfect tense",
                     "example": "I haven\'t seen the film, but she may have done"},
                ]
            }, result)

    def test_third_gram_group_returns_full_content(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[2]

        group = GramGroup(dict_parser, gram_group)
        group.build()
        result = group.translate()

        self.assertEqual(
            {
                "value": "auxiliary verb",
                "defs": [
                    {"def": "used to give emphasis, or as a legal convention", "example": "do stay a while, do hereby enjoin"},
                    {"def": "used to ask a question", "example": "did you write?"},
                    {"def": "used to serve as part of a negative command or statement", "example": "do not go, they do not like it"},
                    {"def": "used to serve as a substitute verb", "example": "love me as I do (love) you"},
                    {"def": "used to form inverted constructions after some adverbs", "example": "little did he realize"},
                ]
            }, result)

    def test_fourth_gram_group_returns_full_content(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[3]

        group = GramGroup(dict_parser, gram_group)
        group.build()
        result = group.translate()

        self.assertEqual(
            {
                "word_forms": ["do's", "dos"],
                "value": "noun",
                "defs": [
                    {"category": "mainly British, informal", "def": "a hoax; swindle"},
                    {"category": "mainly British, informal", "def": "a party or social event"},
                    {"category": "slang", "def":"excrement; feces", "example": "dog do"},
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
            {"word": "do",
             "related": ["do a deal", "do by", "do down", "do in", "do it", "do over", "do's and don'ts",
                         "do up", "do up right", "do oneself well", "do with", "do without", "have to do with"],
             "gram_groups": [
                 {
                    "word_forms": ["did", "done", "doing"],
                    "value": "transitive verb",
                    "defs": [
                        {"def_subgroup": [
                            {"def": "to execute; effect; perform (an act, action, etc.)", "example": "do great deeds"},
                            {"def": "to carry out; fulfill", "example": "do what I tell you"}
                        ]},
                        {"def": "to bring to completion; finish", "example": "dinner has been done for an hour"},
                        {"def": "to bring about; cause; produce", "example": "it does no harm; who did this to you?"},
                        {"def": "to exert (efforts, etc.)", "example": "do your best"},
                        {"def": "to have or take (a meal)", "example": "let\'s do lunch"},
                        {"def": "to deal with as is required; attend to", "example": "do the ironing, do one\'s nails or hair"},
                        {"def": "to have as one\'s work or occupation; work at or on", "example": "what does he do for a living?"},
                        {"def": "to work out; solve", "example": "do a problem"},
                        {"def": "to produce or appear in (a play, etc.)", "example": "we did Hamlet"},
                        {"def_subgroup": [
                            {"def": "to play the role of", "example": "I did Polonius"},
                            {"category": "informal", "def": "to imitate, or behave characteristically as", "example": "to do a Houdini"},
                        ]},
                        {"def": "to write or publish (a book), compose (a musical score), etc."},
                        {"def_subgroup": [
                            {"def": "to cover (distance)", "example": "to do a mile in four minutes"},
                            {"def": "to move along at a speed of", "example": "to do 60 miles an hour"},
                        ]},
                        {"def": "to visit as a sightseer; tour", "example": "they did England in two months"},
                        {"def": "to translate", "example": "to do Horace into English"},
                        {"def": "to give; render", "example": "to do honor to the dead"},
                        {"def": "to suit; be convenient to", "example": "this will do me very well"},
                        {"category": "informal", "def_subgroup": [
                            {"def": "to prepare; cook", "example": "that restaurant does ribs really well"},
                            {"def": "to eat", "example": "let\'s do Mexican tonight"},
                        ]},
                        {"category": "informal", "def": "to cheat; swindle", "example": "you\'ve been done"},
                        {"category": "informal", "def": "to serve (a jail term)"},
                        {"category": "slang", "def": "to take; ingest; use", "example": "we\'ve never done drugs"},
                        {"category": "slang", "def": "to perform a sexual act upon; specif., to have sexual intercourse with"},
                        {"category": "slang", "def": "to kill"},
                    ]
                },
                {
                    "value": "intransitive verb",
                    "defs": [
                        {"def": "to act in a specified way; behave", "example": "he does well when treated well"},
                        {"def": "to be active; work", "example": "do; don\'t merely talk"},
                        {"def": "to finish", "category": "used in the perfect tense [have done with dreaming ]"},
                        {"def": "to get along; fare", "example": "mother and child are doing well"},
                        {"def": "to be adequate or suitable; serve the purpose", "example": "the black dress will do"},
                        {"def": "to take place; go on", "example": "anything doing tonight?"},
                        {"category": "mainly British, informal", "def": "used as a substitute verb after a modal auxiliary or a form of have in a perfect tense",
                         "example": "I haven\'t seen the film, but she may have done"},
                    ]
                },
                {
                    "value": "auxiliary verb",
                    "defs": [
                        {"def": "used to give emphasis, or as a legal convention", "example": "do stay a while, do hereby enjoin"},
                        {"def": "used to ask a question", "example": "did you write?"},
                        {"def": "used to serve as part of a negative command or statement", "example": "do not go, they do not like it"},
                        {"def": "used to serve as a substitute verb", "example": "love me as I do (love) you"},
                        {"def": "used to form inverted constructions after some adverbs", "example": "little did he realize"},
                    ]
                },
                {
                    "word_forms": ["do's", "dos"],
                    "value": "noun",
                    "defs": [
                        {"category": "mainly British, informal", "def": "a hoax; swindle"},
                        {"category": "mainly British, informal", "def": "a party or social event"},
                        {"category": "slang", "def":"excrement; feces", "example": "dog do"},
                    ]
                }
            ]}, result)

    def test_second_def_group_returns_full_content(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[1]

        group = DefGroup(dict_parser, def_group)
        group.build()
        result = group.translate()
        self.assertEqual(
            {"word": "do", "gram_groups": [
                {
                    "value": "noun",
                    "defs": [
                        {"category": "music", "def": "a syllable representing the first or last tone of the diatonic scale"}
                    ]
                },
            ]}, result)

    def test_third_def_group_returns_full_content(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[2]

        group = DefGroup(dict_parser, def_group)
        group.build()
        result = group.translate()
        self.assertEqual(
            {"word": "do", "gram_groups": [
                {
                    "value": "noun",
                    "defs": [
                        {"category": "slang", "def": "hairdo"}
                    ]
                },
            ]}, result)

    def test_fourth_def_group_returns_full_content(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[3]

        group = DefGroup(dict_parser, def_group)
        group.build()
        result = group.translate()
        self.assertEqual(
            {"word": "Do or do", "gram_groups": [
                {
                    "defs": [
                        {"def": "ditto"}
                    ]
                },
            ]}, result)

    def test_fifth_def_group_returns_full_content(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[4]

        group = DefGroup(dict_parser, def_group)
        group.build()
        result = group.translate()
        self.assertEqual(
            {"word": "DO or D.O.", "gram_groups": [
                {
                    "defs": [
                        {"def": "Doctor of Osteopathy"}
                    ]
                }
            ]}, result)

    def test_translate_def_groups(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)

        groups = DefGroups(dict_parser)
        groups.build()
        result = groups.translate()
        self.assertEqual(
            [
                {"word": "do",
                 "related": ["do a deal", "do by", "do down", "do in", "do it", "do over", "do's and don'ts",
                             "do up", "do up right", "do oneself well", "do with", "do without", "have to do with"],
                 "gram_groups": [
                    {
                        "word_forms": ["did", "done", "doing"],
                        "value": "transitive verb",
                        "defs": [
                            {"def_subgroup": [
                                {"def": "to execute; effect; perform (an act, action, etc.)", "example": "do great deeds"},
                                {"def": "to carry out; fulfill", "example": "do what I tell you"}
                            ]},
                            {"def": "to bring to completion; finish", "example": "dinner has been done for an hour"},
                            {"def": "to bring about; cause; produce", "example": "it does no harm; who did this to you?"},
                            {"def": "to exert (efforts, etc.)", "example": "do your best"},
                            {"def": "to have or take (a meal)", "example": "let\'s do lunch"},
                            {"def": "to deal with as is required; attend to", "example": "do the ironing, do one\'s nails or hair"},
                            {"def": "to have as one\'s work or occupation; work at or on", "example": "what does he do for a living?"},
                            {"def": "to work out; solve", "example": "do a problem"},
                            {"def": "to produce or appear in (a play, etc.)", "example": "we did Hamlet"},
                            {"def_subgroup": [
                                {"def": "to play the role of", "example": "I did Polonius"},
                                {"category": "informal", "def": "to imitate, or behave characteristically as", "example": "to do a Houdini"},
                            ]},
                            {"def": "to write or publish (a book), compose (a musical score), etc."},
                            {"def_subgroup": [
                                {"def": "to cover (distance)", "example": "to do a mile in four minutes"},
                                {"def": "to move along at a speed of", "example": "to do 60 miles an hour"},
                            ]},
                            {"def": "to visit as a sightseer; tour", "example": "they did England in two months"},
                            {"def": "to translate", "example": "to do Horace into English"},
                            {"def": "to give; render", "example": "to do honor to the dead"},
                            {"def": "to suit; be convenient to", "example": "this will do me very well"},
                            {"category": "informal", "def_subgroup": [
                                {"def": "to prepare; cook", "example": "that restaurant does ribs really well"},
                                {"def": "to eat", "example": "let\'s do Mexican tonight"},
                            ]},
                            {"category": "informal", "def": "to cheat; swindle", "example": "you\'ve been done"},
                            {"category": "informal", "def": "to serve (a jail term)"},
                            {"category": "slang", "def": "to take; ingest; use", "example": "we\'ve never done drugs"},
                            {"category": "slang", "def": "to perform a sexual act upon; specif., to have sexual intercourse with"},
                            {"category": "slang", "def": "to kill"},
                        ]
                    },
                    {
                        "value": "intransitive verb",
                        "defs": [
                            {"def": "to act in a specified way; behave", "example": "he does well when treated well"},
                            {"def": "to be active; work", "example": "do; don\'t merely talk"},
                            {"def": "to finish", "category": "used in the perfect tense [have done with dreaming ]"},
                            {"def": "to get along; fare", "example": "mother and child are doing well"},
                            {"def": "to be adequate or suitable; serve the purpose", "example": "the black dress will do"},
                            {"def": "to take place; go on", "example": "anything doing tonight?"},
                            {"category": "mainly British, informal", "def": "used as a substitute verb after a modal auxiliary or a form of have in a perfect tense",
                             "example": "I haven\'t seen the film, but she may have done"},
                        ]
                    },
                    {
                        "value": "auxiliary verb",
                        "defs": [
                            {"def": "used to give emphasis, or as a legal convention", "example": "do stay a while, do hereby enjoin"},
                            {"def": "used to ask a question", "example": "did you write?"},
                            {"def": "used to serve as part of a negative command or statement", "example": "do not go, they do not like it"},
                            {"def": "used to serve as a substitute verb", "example": "love me as I do (love) you"},
                            {"def": "used to form inverted constructions after some adverbs", "example": "little did he realize"},
                        ]
                    },
                    {
                        "word_forms": ["do's", "dos"],
                        "value": "noun",
                        "defs": [
                            {"category": "mainly British, informal", "def": "a hoax; swindle"},
                            {"category": "mainly British, informal", "def": "a party or social event"},
                            {"category": "slang", "def":"excrement; feces", "example": "dog do"},
                        ]
                    }
                ]},
                {"word": "do", "gram_groups": [
                    {
                        "value": "noun",
                        "defs": [ {"category": "music", "def": "a syllable representing the first or last tone of the diatonic scale"} ]
                    },
                ]},
                {"word": "do", "gram_groups": [
                    {
                        "value": "noun",
                        "defs": [ {"category": "slang", "def": "hairdo"} ]
                    },
                ]},
                {"word": "Do or do", "gram_groups": [
                    {
                        "defs": [ {"def": "ditto"} ]
                    },
                ]},
                {"word": "DO or D.O.", "gram_groups": [
                    {
                        "defs": [ {"def": "Doctor of Osteopathy"} ]
                    }
                ]}
            ], result)

    def test_word_returns_examples(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)

        group = ExamplesGroup(dict_parser)
        group.build()
        result = group.translate()
        self.assertEqual([
                {"example": "You should write the general principles down somewhere, Dad, like they do with the United States Code."}
            ], result)

    def test_word_returns_nearby_words(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)

        group = NearbyWordsGroup(dict_parser)
        group.build()
        result = group.translate()
        self.assertEqual([
                'Dn', 'DNA', 'DNA fingerprinting', 'DNB', 'Dnepr','Dneprodzerzhinsk', 'Dnepropetrovsk',
                'Dnestr', 'Dnieper', 'Dniester', 'do a deal', 'do a number on', 'do away with', 'do business with',
                'do by', 'do credit to', 'do down', 'do duty for', 'do gree', 'do honor to'], result)

    def test_word_returns_related_defgroup_1(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]

        group = RelatedGroup(dict_parser, def_group)
        group.build()
        result = group.translate()
        self.assertEqual(["do a deal", "do by", "do down", "do in", "do it", "do over", "do's and don'ts",
                                      "do up", "do up right", "do oneself well", "do with", "do without",
                                      "have to do with"], result)

    def test_translate_html_to_json(self):
        obj = HtmlToJson(self.word_name, self.html_content)
        json_str = obj.translate()

        self.assertEqual(json_str,
        {
            "frequency": "Extremely Common",
            "def_groups": [
                {"word": "do", "related": [
                    "do a deal", "do by", "do down", "do in", "do it", "do over", "do's and don'ts", "do up",
                    "do up right", "do oneself well", "do with", "do without", "have to do with"
                ],
                 "gram_groups": [
                     {
                        "word_forms": ["did", "done", "doing"],
                        "value": "transitive verb",
                        "defs": [
                            {"def_subgroup": [
                                {"def": "to execute; effect; perform (an act, action, etc.)", "example": "do great deeds"},
                                {"def": "to carry out; fulfill", "example": "do what I tell you"}
                            ]},
                            {"def": "to bring to completion; finish", "example": "dinner has been done for an hour"},
                            {"def": "to bring about; cause; produce", "example": "it does no harm; who did this to you?"},
                            {"def": "to exert (efforts, etc.)", "example": "do your best"},
                            {"def": "to have or take (a meal)", "example": "let\'s do lunch"},
                            {"def": "to deal with as is required; attend to", "example": "do the ironing, do one\'s nails or hair"},
                            {"def": "to have as one\'s work or occupation; work at or on", "example": "what does he do for a living?"},
                            {"def": "to work out; solve", "example": "do a problem"},
                            {"def": "to produce or appear in (a play, etc.)", "example": "we did Hamlet"},
                            {"def_subgroup": [
                                {"def": "to play the role of", "example": "I did Polonius"},
                                {"category": "informal", "def": "to imitate, or behave characteristically as", "example": "to do a Houdini"},
                            ]},
                            {"def": "to write or publish (a book), compose (a musical score), etc."},
                            {"def_subgroup": [
                                {"def": "to cover (distance)", "example": "to do a mile in four minutes"},
                                {"def": "to move along at a speed of", "example": "to do 60 miles an hour"},
                            ]},
                            {"def": "to visit as a sightseer; tour", "example": "they did England in two months"},
                            {"def": "to translate", "example": "to do Horace into English"},
                            {"def": "to give; render", "example": "to do honor to the dead"},
                            {"def": "to suit; be convenient to", "example": "this will do me very well"},
                            {"category": "informal", "def_subgroup": [
                                {"def": "to prepare; cook", "example": "that restaurant does ribs really well"},
                                {"def": "to eat", "example": "let\'s do Mexican tonight"},
                            ]},
                            {"category": "informal", "def": "to cheat; swindle", "example": "you\'ve been done"},
                            {"category": "informal", "def": "to serve (a jail term)"},
                            {"category": "slang", "def": "to take; ingest; use", "example": "we\'ve never done drugs"},
                            {"category": "slang", "def": "to perform a sexual act upon; specif., to have sexual intercourse with"},
                            {"category": "slang", "def": "to kill"},
                        ]
                    },
                    {
                        "value": "intransitive verb",
                        "defs": [
                            {"def": "to act in a specified way; behave", "example": "he does well when treated well"},
                            {"def": "to be active; work", "example": "do; don\'t merely talk"},
                            {"def": "to finish", "category": "used in the perfect tense [have done with dreaming ]"},
                            {"def": "to get along; fare", "example": "mother and child are doing well"},
                            {"def": "to be adequate or suitable; serve the purpose", "example": "the black dress will do"},
                            {"def": "to take place; go on", "example": "anything doing tonight?"},
                            {"category": "mainly British, informal", "def": "used as a substitute verb after a modal auxiliary or a form of have in a perfect tense",
                             "example": "I haven\'t seen the film, but she may have done"},
                        ]
                    },
                    {
                        "value": "auxiliary verb",
                        "defs": [
                            {"def": "used to give emphasis, or as a legal convention", "example": "do stay a while, do hereby enjoin"},
                            {"def": "used to ask a question", "example": "did you write?"},
                            {"def": "used to serve as part of a negative command or statement", "example": "do not go, they do not like it"},
                            {"def": "used to serve as a substitute verb", "example": "love me as I do (love) you"},
                            {"def": "used to form inverted constructions after some adverbs", "example": "little did he realize"},
                        ]
                    },
                    {
                        "word_forms": ["do's", "dos"],
                        "value": "noun",
                        "defs": [
                            {"category": "mainly British, informal", "def": "a hoax; swindle"},
                            {"category": "mainly British, informal", "def": "a party or social event"},
                            {"category": "slang", "def":"excrement; feces", "example": "dog do"},
                        ]
                    }
                ]},
                {"word": "do", "gram_groups": [
                    {
                        "value": "noun",
                        "defs": [ {"category": "music", "def": "a syllable representing the first or last tone of the diatonic scale"} ]
                    },
                ]},
                {"word": "do", "gram_groups": [
                    {
                        "value": "noun",
                        "defs": [ {"category": "slang", "def": "hairdo"} ]
                    },
                ]},
                {"word": "Do or do", "gram_groups": [
                    {
                        "defs": [ {"def": "ditto"} ]
                    },
                ]},
                {"word": "DO or D.O.", "gram_groups": [
                    {
                        "defs": [ {"def": "Doctor of Osteopathy"} ]
                    }
                ]}
            ],
            "examples": [
                {"example": "You should write the general principles down somewhere, Dad, like they do with the United States Code."}
            ],
            "nearby_words": [
                'Dn', 'DNA', 'DNA fingerprinting', 'DNB', 'Dnepr','Dneprodzerzhinsk', 'Dnepropetrovsk',
                'Dnestr', 'Dnieper', 'Dniester', 'do a deal', 'do a number on', 'do away with', 'do business with',
                'do by', 'do credit to', 'do down', 'do duty for', 'do gree', 'do honor to'
            ]
        })

