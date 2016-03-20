import unittest
from unittest.mock import patch
from def_groups import *
from dict_parse import DictParser
import html_to_json
from html_to_json import HtmlToJson
from lxml import etree


class HtmlToJsonTest(unittest.TestCase):

    def setUp(self):
        f = open("perform_defs.html")
        self.word_name = "perform"

        self.html_content = f.read()
        # self.maxDiff = None

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

        with patch('html_to_json.DefGroup.build') as mock:
            mock.return_value = None
            group = DefGroup(dict_parser, etree_group)
            group.build()
            result = group.translate()
            self.assertEqual({"word": "perform", "gram_groups": []}, result)

    # word / def_groups
    def test_def_groups_returns_1_def_group(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)

        with patch('html_to_json.DefGroup.build'):
            group = DefGroups(dict_parser)
            group.build()
            result = group.translate()
            self.assertEqual([{"word": "perform", "gram_groups": []}],
                result)

    # word / def_groups / def_group [0] / gram_groups
    def test_first_def_group_returns_2_gram_groups(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]

        with patch('html_to_json.GramGroup.build'):
            with patch('html_to_json.RelatedGroup.build'):
                group = DefGroup(dict_parser, def_group)
                group.build()
                result = group.translate()
                self.assertEqual(
                    {"word": "perform", "gram_groups": [{}, {}],
                     "semantics": "perform, often a mere formal equivalent for do, is usually used of a more or less involved process "
                     "rather than a single act [to perform an experiment ]; execute implies a putting into effect or completing "
                     "that which has been planned or ordered [to execute a law ]; accomplish suggests effort and perseverance in "
                     "carrying out a plan or purpose [to accomplish a mission ]; achieve implies the overcoming of obstacles in "
                     "accomplishing something of worth or importance [to achieve a lasting peace ]; effect also suggests the "
                     "conquering of difficulties but emphasizes what has been done to bring about the result [his cure was "
                     "effected by the use of certain drugs ]; fulfill, in strict discrimination, implies the full realization of "
                     "what is expected or demanded [to fulfill a promise ]"},
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
                "value": "transitive verb",
                "defs": []}, result)

    def test_defs_group_0_returns_3_empty_items(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[0]

        with patch('html_to_json.WordDefinition.build'):
            group = SenseListGroup(dict_parser, gram_group)
            group.build()
            result = group.translate()
            self.assertEqual([{"def": ""}, {"def": ""}, {"def": ""}], result)

    def test_def_returns_def_json(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[0]
        sslist = dict_parser.get_senselist(gram_group)
        sslitem = dict_parser.get_all_senselist_items(sslist)[2]

        group = WordDefinition(dict_parser, sslitem)
        group.build()
        result = group.translate()
        self.assertEqual({"def": "to give a performance of; render or enact (a piece of music, a dramatic role, etc.)"},
                         result)

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
            {"def": "to act on so as to accomplish or bring to completion; execute; carry out (a task, process, etc.)"},
            {"def": "to carry out; meet the requirements of; fulfill (a promise, command, etc.)"},
            {"def": "to give a performance of; render or enact (a piece of music, a dramatic role, etc.)"},

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
                "value": "transitive verb",
                "defs": [
                    {"def": "to act on so as to accomplish or bring to completion; execute; carry out (a task, process, etc.)"},
                    {"def": "to carry out; meet the requirements of; fulfill (a promise, command, etc.)"},
                    {"def": "to give a performance of; render or enact (a piece of music, a dramatic role, etc.)"},
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
                    {"def": "to carry out or execute an action or process; esp., to take part in a musical program, "
                     "act in a play, dance, etc. before an audience"},
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
            {"word": "perform",
             "gram_groups": [
                 {
                     "value": "transitive verb",
                     "defs": [
                         {"def": "to act on so as to accomplish or bring to completion; execute; carry out (a task, process, etc.)"},
                         {"def": "to carry out; meet the requirements of; fulfill (a promise, command, etc.)"},
                         {"def": "to give a performance of; render or enact (a piece of music, a dramatic role, etc.)"},
                     ]
                 },
                 {
                     "value": "intransitive verb",
                     "defs": [
                         {"def": "to carry out or execute an action or process; esp., to take part in a musical program, "
                                 "act in a play, dance, etc. before an audience"},
                     ]
                 },
             ],
             "semantics":
                 "perform, often a mere formal equivalent for do, is usually used of a more or less involved process "
                 "rather than a single act [to perform an experiment ]; execute implies a putting into effect or completing "
                 "that which has been planned or ordered [to execute a law ]; accomplish suggests effort and perseverance in "
                 "carrying out a plan or purpose [to accomplish a mission ]; achieve implies the overcoming of obstacles in "
                 "accomplishing something of worth or importance [to achieve a lasting peace ]; effect also suggests the "
                 "conquering of difficulties but emphasizes what has been done to bring about the result [his cure was "
                 "effected by the use of certain drugs ]; fulfill, in strict discrimination, implies the full realization of "
                 "what is expected or demanded [to fulfill a promise ]"
             }, result)

    def test_translate_def_groups(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)

        groups = DefGroups(dict_parser)
        groups.build()
        result = groups.translate()
        self.assertEqual(
            [
                {"word": "perform",
                 "semantics":
                     "perform, often a mere formal equivalent for do, is usually used of a more or less involved process "
                     "rather than a single act [to perform an experiment ]; execute implies a putting into effect or completing "
                     "that which has been planned or ordered [to execute a law ]; accomplish suggests effort and perseverance in "
                     "carrying out a plan or purpose [to accomplish a mission ]; achieve implies the overcoming of obstacles in "
                     "accomplishing something of worth or importance [to achieve a lasting peace ]; effect also suggests the "
                     "conquering of difficulties but emphasizes what has been done to bring about the result [his cure was "
                     "effected by the use of certain drugs ]; fulfill, in strict discrimination, implies the full realization of "
                     "what is expected or demanded [to fulfill a promise ]",
                 "gram_groups": [
                     {
                         "value": "transitive verb",
                         "defs": [
                             {"def": "to act on so as to accomplish or bring to completion; execute; carry out (a task, process, etc.)"},
                             {"def": "to carry out; meet the requirements of; fulfill (a promise, command, etc.)"},
                             {"def": "to give a performance of; render or enact (a piece of music, a dramatic role, etc.)"},
                         ]
                     },
                     {
                         "value": "intransitive verb",
                         "defs": [
                             {"def": "to carry out or execute an action or process; esp., to take part in a musical program, "
                              "act in a play, dance, etc. before an audience"},
                         ]
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
                {"example": "I believe she would have been able to perform the operation."}
            ], result)

    def test_word_returns_nearby_words(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)

        group = NearbyWordsGroup(dict_parser)
        group.build()
        result = group.translate()
        self.assertEqual([
            "perfecto", "perfervid", "perfidious", "perfidy", "perfoliate", "perforate", "perforated", "perforation",
            "perforative", "perforce", "performance", "performance art", "performative", "performing arts", "perfume",
            "perfumer", "perfumery", "perfunctory", "perfuse", "perfusionist"], result)

    def test_word_returns_related_defgroup_1_empty(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]

        group = RelatedGroup(dict_parser, def_group)
        group.build()
        result = group.translate()
        self.assertEqual([], result)

    def test_translate_html_to_json(self):
        obj = HtmlToJson(self.word_name, self.html_content)
        json_str = obj.translate()

        self.assertEqual(json_str,
        {
            "frequency": "Very Common",
            "def_groups": [
                {"word": "perform",
                 "semantics":
                     "perform, often a mere formal equivalent for do, is usually used of a more or less involved process "
                     "rather than a single act [to perform an experiment ]; execute implies a putting into effect or completing "
                     "that which has been planned or ordered [to execute a law ]; accomplish suggests effort and perseverance in "
                     "carrying out a plan or purpose [to accomplish a mission ]; achieve implies the overcoming of obstacles in "
                     "accomplishing something of worth or importance [to achieve a lasting peace ]; effect also suggests the "
                     "conquering of difficulties but emphasizes what has been done to bring about the result [his cure was "
                     "effected by the use of certain drugs ]; fulfill, in strict discrimination, implies the full realization of "
                     "what is expected or demanded [to fulfill a promise ]",
                 "gram_groups": [
                     {
                         "value": "transitive verb",
                         "defs": [
                             {"def": "to act on so as to accomplish or bring to completion; execute; carry out (a task, process, etc.)"},
                             {"def": "to carry out; meet the requirements of; fulfill (a promise, command, etc.)"},
                             {"def": "to give a performance of; render or enact (a piece of music, a dramatic role, etc.)"},
                         ]
                     },
                     {
                         "value": "intransitive verb",
                         "defs": [
                             {"def": "to carry out or execute an action or process; esp., to take part in a musical program, "
                              "act in a play, dance, etc. before an audience"},
                         ]
                     }
                 ]}
            ],
            "examples": [
                {"example": "I believe she would have been able to perform the operation."}
            ],
            "nearby_words": [
                "perfecto", "perfervid", "perfidious", "perfidy", "perfoliate", "perforate", "perforated", "perforation",
                "perforative", "perforce", "performance", "performance art", "performative", "performing arts", "perfume",
                "perfumer", "perfumery", "perfunctory", "perfuse", "perfusionist"
            ]
        })

