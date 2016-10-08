import unittest
import os
from unittest.mock import patch
from src.def_groups import *
from src.def_parser import DefParser
from lxml import etree

from src.html_parser import HtmlParser
from src import config


class HtmlToJsonTest(unittest.TestCase):
    word_name = ""
    html_content = ""

    @classmethod
    def setUpClass(cls):
        file_name = os.path.join(config.HTML_SOURCE_PATH, "do_defs.html")

        with open(file_name) as f:
            cls.word_name = "do"
            cls.html_content = f.read()

        # self.maxDiff = None

    def test_createHtmlToJson_obj(self):
        obj = HtmlParser()
        self.assertIsNotNone(obj)

    def test_translateEmptyMain_toJson_returnsEmptyWord(self):
        obj = HtmlParser()

        with patch.object(MainDefGroup, 'build_children') as mock:
            mock.return_value = None
            json_obj = obj.parse(self.word_name, self.html_content)
            MainDefGroup.build_children.assert_called_once_with()
            self.assertEqual(json_obj, {})

    # word / def_groups
    def test_defGroups_returns_emptyGroups(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)

        with patch.object(DefGroups, 'build'):
            group = DefGroups(dict_parser)
            group.build()
            result = group.translate()
            self.assertEqual([], result)

    # word / def_groups / def_group [0]
    def test_defGroup_returnsEmpty(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        etree_group = dict_parser.get_all_def_groups()[0]

        with patch.object(DefGroup, 'build'):
            group = DefGroup(dict_parser, etree_group)
            group.build()
            result = group.translate()
            self.assertEqual({'gram_groups': [], 'word': 'do'}, result)

    def test_wordFreq_is_extremelyCommon(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        etree_group = dict_parser.get_all_def_groups()[0]

        group = WordFrequencyGroup(dict_parser, etree_group)
        group.build()
        result = group.translate()
        self.assertEqual(result, "Extremely Common")

    # word / def_groups / def_group [0]
    def test_defGroup0_returns_noItems(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        etree_group = dict_parser.get_all_def_groups()[0]

        with patch.object(DefGroup, 'build') as mock:
            mock.return_value = None
            group = DefGroup(dict_parser, etree_group)
            group.build()
            result = group.translate()
            self.assertEqual({"word": "do", "gram_groups": []}, result)

    # word / def_groups
    def test_defGroups_returns_5_defGroups(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)

        with patch.object(DefGroup, 'build'):
            group = DefGroups(dict_parser)
            group.build()
            result = group.translate()
            self.assertEqual([
                {"word": "do", "gram_groups": []}, {"word": "do or do a", "gram_groups": []},
                {"word": "do", "gram_groups": []}, {"word": "do", "gram_groups": []},
                {"word": "DO", "gram_groups": []}, {"word": "do.", "gram_groups": []}],
                result)

    # word / def_groups / def_group [0] / gram_groups
    def test_defGroup0_returns_2_gramGroups(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]

        with patch.object(GramGroup, 'build'):
            group = DefGroup(dict_parser, def_group)
            group.build()
            result = group.translate()

            self.assertEqual({"frequency": "Extremely Common", "word": "do", "gram_groups": [{}, {}],
                              "origin":
                                  "Old English dōn; related to Old Frisian duān, Old High German tuon, Latin abdere "
                                  "to put away, Greek tithenai to place; see deed, doom"},
                             result)

    # word / def_groups / def_group [0] / gram_group[0]
    def test_gramGroup0_returns_3_children(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[0]

        with patch.object(UsageGroups, "build"):
            group = GramGroup(dict_parser, gram_group)
            group.build()
            result = group.translate()

            self.assertEqual({
                "forms": {"items": ["does", "doing", "did", "done"], "info": ""},
                "value": "verb",
                "defs": {}
            }, result)

    def test_def_noSpecifiedUsage(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[1]
        sense = dict_parser.get_all_sense_items(gram_group)[0]

        word = WordDefinition(dict_parser, sense)
        word.build()
        result = word.translate()

        self.assertEqual({"category": "slang", "def": "an act or instance of cheating or swindling", "mark": "good"}, result)

    def test_def_withSpecifiedUsage(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[0]
        sense = dict_parser.get_all_sense_items(gram_group)[1]

        word = WordDefinition(dict_parser, sense)
        word.build()
        result = word.get_usage()

        self.assertEqual("often intr; foll by for", result)

    def test_usageGroups(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[0]
        senses = dict_parser.get_all_sense_items(gram_group)

        usages = UsageGroups(dict_parser, senses)
        usages.build()
        usg_names = usages.names()

        self.assertEqual({
            "often intr; foll by for",
            "transitive",
            "intransitive",
            "takes an infinitive without to",
            ""
        }, usg_names)

    def test_firstUsageGroups(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[0]
        senses = dict_parser.get_all_sense_items(gram_group)

        usages = UsageGroups(dict_parser, senses)
        usages.build()
        result = usages.translate()

        self.assertEqual([{
            "def": "to serve the needs of; be suitable for (a person, situation, etc); suffice",
            "example": "there isn't much food, but it'll do for the two of us",
            "mark": "good",
        }],
            result["often intr; foll by for"])

    def test_defSubgroup(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[0]
        sense = dict_parser.get_all_sense_items(gram_group)[27]

        group = WordDefinition(dict_parser, sense)
        group.build()
        result = group.translate()

        self.assertEqual({
            "category": "slang",
            "def_subgroup": [
                {"def": "to arrest", "mark": "good"},
                {"def": "to convict of a crime", "mark": "good"}
        ]}, result)

    def test_gramGroup0_fullContent(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[0]

        group = GramGroup(dict_parser, gram_group)
        group.build()
        result = group.translate()

        self.assertEqual({
            "forms": {"items": ["does", "doing", "did", "done"], "info": ""},
            "value": "verb",
            "defs": {
                "": [
                    {
                        "def": "to perform or complete (a deed or action)",
                        "example": "to do a portrait; the work is done",
                        "mark": "good"
                    },
                    {
                        "def": "used as an auxiliary to replace an earlier verb or verb phrase to avoid repetition",
                        "example": "he likes you as much as I do",
                        "mark": "good"
                    },
                    {"def": "(i) See do", "mark": "good"},
                    {"def": "(i) See do or die", "mark": "good"},
                    {"def": "(i) See how do you do?", "mark": "good"},
                    {"def": "(i) See make do", "mark": "good"},
                ],
                "often intr; foll by for": [
                    {
                        "def": "to serve the needs of; be suitable for (a person, situation, etc); suffice",
                        "example": "there isn't much food, but it'll do for the two of us",
                        "mark": "good"
                    },
                ],
                "transitive": [
                    {"def": "to arrange or fix", "example": "you should do the garden now", "mark": "good"},
                    {"def": "to prepare or provide; serve", "example": "this restaurant doesn't do lunch on Sundays",
                     "mark": "good"},
                    {"def": "to make tidy, elegant, ready, etc, as by arranging or adorning",
                     "example": "to do one's hair", "mark": "good"},
                    {"def": "to improve (esp in the phrase do something to or for)", "mark": "good"},
                    {"def": "to find an answer to (a problem or puzzle)", "mark": "good"},
                    {"def": "to translate or adapt the form or language of", "example": "the book was done into a play",
                     "mark": "good"},
                    {"def": "to cause or produce", "example": "complaints do nothing to help", "mark": "good"},
                    {"def": "to give or render", "example": "your portrait doesn't do you justice; do me a favour",
                     "mark": "good"},
                    {"def": "to work at, esp as a course of study or a profession", "example": "he is doing chemistry; "
                     "what do you do for a living?", "mark": "good"},
                    {"def": "to perform (a play, etc); act", "example": "they are doing 'Hamlet' next week",
                     "mark": "good"},
                    {"def": "to travel at a specified speed, esp as a maximum", "example": "this car will do 120 mph",
                     "mark": "good"},
                    {"def": "to travel or traverse (a distance)", "example": "we did 15 miles on our walk",
                     "mark": "good"},
                    {
                        "category": "informal",
                        "def": "to visit or explore as a sightseer or tourist",
                        "example": "to do Westminster Abbey",
                        "mark": "good"
                    },
                    {"def": "to wear out; exhaust", "mark": "good"},
                    {
                        "category": "slang",
                        "def": "to serve (a period of time) as a prison sentence",
                        "example": "he's doing three years for burglary; he's doing time",
                        "mark": "good"
                    },
                    {"category": "informal", "def": "to cheat or swindle", "mark": "good"},
                    {"category": "slang", "def": "to rob", "example": "they did three shops last night", "mark": "good"},
                    {
                        "category": "slang",
                        "def_subgroup": [
                            {"def": "to arrest", "mark": "good"},
                            {"def": "to convict of a crime", "mark": "good"}
                        ]
                    },
                    {"category": "Australian informal", "def": "to lose or spend (money) completely", "mark": "good"},
                    {"category": "slang, mainly British", "def": "to treat violently; assault", "mark": "good"},
                    {"category": "slang", "def": "to take or use (a drug)", "mark": "good"},
                    {"category": "taboo, slang", "def": "(of a male) to have sexual intercourse with", "mark": "good"},
                    {"def": "to arrange (a meal)", "example": "let's do lunch", "mark": "good"},
                ],
                "intransitive": [
                    {"def": "to conduct oneself", "example": "do as you please", "mark": "good"},
                    {"def": "to fare or manage", "example": "how are you doing these days?", "mark": "good"},
                    {"def": "to happen (esp in the phrase nothing doing)", "mark": "good"},
                ],
                "takes an infinitive without to": [
                    {
                        "def": "used as an auxiliary before the subject of an interrogative sentence as a way of "
                               "forming a question",
                        "example": "do you agree?; when did John go out?", "mark": "good"
                    },
                    {
                        "def": "used as an auxiliary to intensify positive statements and commands",
                        "example": "I do like your new house; do hurry!", "mark": "good"
                    },
                    {
                        "def": "used as an auxiliary before a negative adverb to form negative statements or commands",
                        "example": "he does not like cheese; do not leave me here alone!", "mark": "good"
                    },
                    {
                        "def": "used as an auxiliary in inverted constructions",
                        "example": "little did he realize that; only rarely does he come in before ten o'clock",
                        "mark": "good"
                    },
                ]
            }
        }, result)

    def test_gramGroup1_fullContent(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[1]

        group = GramGroup(dict_parser, gram_group)
        group.build()
        result = group.translate()

        self.assertEqual({
            "forms": {"items": ["dos", "do's"], "info": "plural"},
            "value": "noun",
            "defs": {
                "": [
                    {"category": "slang", "def": "an act or instance of cheating or swindling", "mark": "good"},
                    {
                        "category": "informal, mainly British and New Zealand",
                        "def": "a formal or festive gathering; party",
                        "mark": "good"
                    },
                    {"def": "(i) See do's and don'ts", "mark": "good"},
                ]
            }
        }, result)

    def test_defGroup0_fullContent(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]

        group = DefGroup(dict_parser, def_group)
        group.build()
        result = group.translate()

        self.assertEqual(
            {"word": "do",
             "origin": "Old English dōn; related to Old Frisian duān, Old High German tuon, Latin abdere "
                       "to put away, Greek tithenai to place; see deed, doom",
             "frequency": "Extremely Common",
             "gram_groups": [
                 {
                     "forms": {"items": ["does", "doing", "did", "done"], "info": ""},
                     "value": "verb",
                     "defs": {
                         "": [
                             {
                                 "def": "to perform or complete (a deed or action)",
                                 "example": "to do a portrait; the work is done",
                                 "mark": "good"
                             },
                             {
                                 "def": "used as an auxiliary to replace an earlier verb or verb phrase to avoid repetition",
                                 "example": "he likes you as much as I do",
                                 "mark": "good"
                             },
                             {"def": "(i) See do", "mark": "good"},
                             {"def": "(i) See do or die", "mark": "good"},
                             {"def": "(i) See how do you do?", "mark": "good"},
                             {"def": "(i) See make do", "mark": "good"},
                         ],
                         "often intr; foll by for": [
                             {
                                 "def": "to serve the needs of; be suitable for (a person, situation, etc); suffice",
                                 "example": "there isn't much food, but it'll do for the two of us",
                                 "mark": "good"
                             },
                         ],
                         "transitive": [
                             {"def": "to arrange or fix", "example": "you should do the garden now", "mark": "good"},
                             {"def": "to prepare or provide; serve",
                              "example": "this restaurant doesn't do lunch on Sundays",
                              "mark": "good"},
                             {"def": "to make tidy, elegant, ready, etc, as by arranging or adorning",
                              "example": "to do one's hair", "mark": "good"},
                             {"def": "to improve (esp in the phrase do something to or for)", "mark": "good"},
                             {"def": "to find an answer to (a problem or puzzle)", "mark": "good"},
                             {"def": "to translate or adapt the form or language of",
                              "example": "the book was done into a play",
                              "mark": "good"},
                             {"def": "to cause or produce", "example": "complaints do nothing to help", "mark": "good"},
                             {"def": "to give or render",
                              "example": "your portrait doesn't do you justice; do me a favour",
                              "mark": "good"},
                             {"def": "to work at, esp as a course of study or a profession",
                              "example": "he is doing chemistry; "
                                         "what do you do for a living?", "mark": "good"},
                             {"def": "to perform (a play, etc); act", "example": "they are doing 'Hamlet' next week",
                              "mark": "good"},
                             {"def": "to travel at a specified speed, esp as a maximum",
                              "example": "this car will do 120 mph",
                              "mark": "good"},
                             {"def": "to travel or traverse (a distance)", "example": "we did 15 miles on our walk",
                              "mark": "good"},
                             {
                                 "category": "informal",
                                 "def": "to visit or explore as a sightseer or tourist",
                                 "example": "to do Westminster Abbey",
                                 "mark": "good"
                             },
                             {"def": "to wear out; exhaust", "mark": "good"},
                             {
                                 "category": "slang",
                                 "def": "to serve (a period of time) as a prison sentence",
                                 "example": "he's doing three years for burglary; he's doing time",
                                 "mark": "good"
                             },
                             {"category": "informal", "def": "to cheat or swindle", "mark": "good"},
                             {"category": "slang", "def": "to rob", "example": "they did three shops last night",
                              "mark": "good"},
                             {
                                 "category": "slang",
                                 "def_subgroup": [
                                     {"def": "to arrest", "mark": "good"},
                                     {"def": "to convict of a crime", "mark": "good"}
                                 ]
                             },
                             {"category": "Australian informal", "def": "to lose or spend (money) completely",
                              "mark": "good"},
                             {"category": "slang, mainly British", "def": "to treat violently; assault", "mark": "good"},
                             {"category": "slang", "def": "to take or use (a drug)", "mark": "good"},
                             {"category": "taboo, slang", "def": "(of a male) to have sexual intercourse with",
                              "mark": "good"},
                             {"def": "to arrange (a meal)", "example": "let's do lunch", "mark": "good"},
                         ],
                         "intransitive": [
                             {"def": "to conduct oneself", "example": "do as you please", "mark": "good"},
                             {"def": "to fare or manage", "example": "how are you doing these days?", "mark": "good"},
                             {"def": "to happen (esp in the phrase nothing doing)", "mark": "good"},
                         ],
                         "takes an infinitive without to": [
                             {
                                 "def": "used as an auxiliary before the subject of an interrogative sentence as a way of "
                                        "forming a question",
                                 "example": "do you agree?; when did John go out?", "mark": "good"
                             },
                             {
                                 "def": "used as an auxiliary to intensify positive statements and commands",
                                 "example": "I do like your new house; do hurry!", "mark": "good"
                             },
                             {
                                 "def": "used as an auxiliary before a negative adverb to form negative statements or commands",
                                 "example": "he does not like cheese; do not leave me here alone!", "mark": "good"
                             },
                             {
                                 "def": "used as an auxiliary in inverted constructions",
                                 "example": "little did he realize that; only rarely does he come in before ten o'clock",
                                 "mark": "good"
                             },
                         ]
                     }
                 },
                 {
                     "forms": {"items": ["dos", "do's"], "info": "plural"},
                     "value": "noun",
                     "defs": {
                         "": [
                             {"category": "slang", "def": "an act or instance of cheating or swindling", "mark": "good"},
                             {
                                 "category": "informal, mainly British and New Zealand",
                                 "def": "a formal or festive gathering; party",
                                 "mark": "good"
                             },
                             {"def": "(i) See do's and don'ts", "mark": "good"},
                         ]
                     }
                 }
             ]}, result)

    def test_defGroup1_fullContent(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[1]

        group = DefGroup(dict_parser, def_group)
        group.build()
        result = group.translate()

        self.assertEqual(
            {"word": "do or do a",
             "frequency": "",
             "gram_groups": [
                 {
                     "forms": {"items": [], "info": ""},
                     "defs": {
                         "": [
                             {
                                 "category": "informal",
                                 "def": "to act like; imitate",
                                 "example": "he's a good mimic – he can do all his friends well",
                                 "mark": "good"
                             },
                         ],
                     }
                 },
             ]}, result)

    def test_defGroup2_fullContent(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[2]

        group = DefGroup(dict_parser, def_group)
        group.build()
        result = group.translate()

        self.assertEqual(
            {"word": "do",
             "frequency": "",
             "gram_groups": [
                 {
                     "forms": {"items": ["dos"], "info": "plural"},
                     "value": "noun",
                     "defs": {
                         "": [
                             {
                                 "def": "(i) a variant spelling of doh",
                                 "mark": "good"
                             },
                         ],
                     }
                 },
             ]}, result)

    def test_defGroup3_fullContent(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[3]

        group = DefGroup(dict_parser, def_group)
        group.build()
        result = group.translate()

        self.assertEqual(
            {"word": "do",
             "frequency": "",
             "gram_groups": [
                 {
                     "forms": {"items": [], "info": ""},
                     "value": "the internet domain name for",
                     "defs": {
                         "": [
                             {
                                 "def": "Dominican Republic",
                                 "mark": "good"
                             },
                         ],
                     }
                 },
             ]}, result)

    def test_defGroup4_fullContent(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[4]

        group = DefGroup(dict_parser, def_group)
        group.build()
        result = group.translate()

        self.assertEqual(
            {"word": "DO",
             "frequency": "",
             "gram_groups": [
                 {
                     "forms": {"items": [], "info": ""},
                     "value": "abbreviation for",
                     "defs": {
                         "": [
                             {"def": "Doctor of Optometry", "mark": "good"},
                             {"def": "Doctor of Osteopathy", "mark": "good"},
                         ],
                     }
                 },
             ]}, result)

    def test_defGroup5_fullContent(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[5]

        group = DefGroup(dict_parser, def_group)
        group.build()
        result = group.translate()

        self.assertEqual(
            {"word": "do.",
             "frequency": "",
             "gram_groups": [
                 {
                     "forms": {"items": [], "info": ""},
                     "value": "abbreviation for",
                     "defs": {"": [{"def": "ditto", "mark": "good"}]}
                 },
             ]}, result)

    def test_examples(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)

        group = ExamplesGroup(dict_parser)
        group.build()
        result = group.translate()

        self.assertEqual([
                "Then again, not to do him down too much, he does have his more positive side.",
                "I'd shouted: You want her to be French, do n't you, you can't stand the idea of Jessica being English!",
                "He was accusing me of being complicit in a murder, or being a murderer, I do n't know which.",
                "\"You should write the general principles down somewhere, Dad, like they do with the United States Code."
            ], result)

    def test_translations(self):
        obj = HtmlParser()
        json_obj = obj.parse(self.word_name, self.html_content)

        self.assertEqual(json_obj["translations"],
                         [{"def": "If you do something, you spend some time on it or finish it.",
                           "example": "I tried to do some work.",
                           "word": "do",
                           "value": "verb",
                           }])

if __name__ == '__main__':
    unittest.main()
