import unittest
from unittest.mock import patch
from src.html_parser.def_groups import *
from src.html_parser.def_parser import DefParser
from lxml import etree


class HtmlToJsonTest(unittest.TestCase):

    def setUp(self):
        f = open("down_defs.html")
        self.word_name = "down"

        self.html_content = f.read()
        # self.maxDiff = None

    def test_word_freq_group_value_is_extremely_common(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)

        group = WordFrequencyGroup(dict_parser)
        group.build()
        result = group.translate()
        self.assertEqual(result, "Extremely Common")

    # word / def_groups
    def test_def_groups_returns_5_def_groups(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)

        with patch.object(DefGroup, 'build'):
            group = DefGroups(dict_parser)
            group.build()
            result = group.translate()
            self.assertEqual([
                {"word": "down", "gram_groups": []}, {"word": "down", "gram_groups": []},
                {"word": "down", "gram_groups": []}, {"word": "Down", "gram_groups": []},
                {"word": "down-", "gram_groups": []}],
                result)

    # word / def_groups / def_group [0] / gram_groups
    def test_first_def_group_returns_6_gram_groups(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]

        with patch.object(GramGroup, 'build'):
            with patch.object(RelatedGroup, 'build'):
                group = DefGroup(dict_parser, def_group)
                group.build()
                result = group.translate()
                self.assertEqual({"word": "down", "gram_groups": [{}, {}, {}, {}, {}, {}]},
                                 result)

    # word / def_groups / def_group [0] / gram_group[0]
    def test_first_gram_group_returns_without_defs(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[0]

        with patch.object(SenseListGroup, 'build'):
            group = GramGroup(dict_parser, gram_group)
            group.build()
            result = group.translate()
            self.assertEqual({
                "value": "adverb",
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
        self.assertEqual({"def": "from a higher to a lower place; toward the ground"}, result)

    def test_def_subgroup_returns_full_defs(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[0]
        sslist = dict_parser.get_senselist(gram_group)
        sslitem = dict_parser.get_all_senselist_items(sslist)[2]

        group = WordDefinition(dict_parser, sslitem)
        group.build()
        result = group.translate()
        self.assertEqual({"def_subgroup": [
            {"def": "in or to a place thought of as lower or below; often, specif., southward",
             "example": "to go down to Florida"},
            {"def": "out of one's hand", "example": "put it down"}
        ]}, result)

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
            {"def": "from a higher to a lower place; toward the ground"},
            {"def": "in, on, or to a lower position or level; specif., to a sitting or reclining position"},
            {"def_subgroup": [
                {"def": "in or to a place thought of as lower or below; often, specif., southward",
                 "example": "to go down to Florida"},
                {"def": "out of one's hand", "example": "put it down"}
            ]},
            {"def": "below the horizon"},
            {"def": "from an earlier to a later period or person", "example": "down through the years"},
            {"def": "into a low or dejected emotional condition"},
            {"def": "into a low or prostrate physical condition", "example": "to come down with a cold"},
            {"def": "in or into an inferior position or condition", "example": "held down by harsh laws"},
            {"def": "to a lower amount, value, or bulk", "example": "to come down in price"},
            {"def_subgroup": [
                {"def": "to a less excited or active condition; into a tranquil or quiet state", "example": "to settle down"},
                {"def": "to a lower volume of sound", "example": "turn down the radio"},
            ]},
            {"def": "in a serious or earnest manner", "example": "to get down to work"},
            {"def": "completely; to the full extent", "example": "loaded down"},
            {"def": "in cash or when bought", "example": "five dollars down and the remainder in installments"},
            {"def": "in writing; on record", "example": "take down his name"},
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
                "value": "adverb",
                "defs": [
                    {"def": "from a higher to a lower place; toward the ground"},
                    {"def": "in, on, or to a lower position or level; specif., to a sitting or reclining position"},
                    {"def_subgroup": [
                        {"def": "in or to a place thought of as lower or below; often, specif., southward",
                         "example": "to go down to Florida"},
                        {"def": "out of one's hand", "example": "put it down"}
                    ]},
                    {"def": "below the horizon"},
                    {"def": "from an earlier to a later period or person", "example": "down through the years"},
                    {"def": "into a low or dejected emotional condition"},
                    {"def": "into a low or prostrate physical condition", "example": "to come down with a cold"},
                    {"def": "in or into an inferior position or condition", "example": "held down by harsh laws"},
                    {"def": "to a lower amount, value, or bulk", "example": "to come down in price"},
                    {"def_subgroup": [
                        {"def": "to a less excited or active condition; into a tranquil or quiet state",
                         "example": "to settle down"},
                        {"def": "to a lower volume of sound", "example": "turn down the radio"},
                    ]},
                    {"def": "in a serious or earnest manner", "example": "to get down to work"},
                    {"def": "completely; to the full extent", "example": "loaded down"},
                    {"def": "in cash or when bought", "example": "five dollars down and the remainder in installments"},
                    {"def": "in writing; on record", "example": "take down his name"},
                ]
            }, result)

    def test_second_ggroup_def_subgroup_football(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[1]
        sslist = dict_parser.get_senselist(gram_group)
        sslitem = dict_parser.get_all_senselist_items(sslist)[10]
        sslitem = dict_parser.get_senselist(sslitem)
        sslitem = dict_parser.get_all_senselist_items(sslitem)[0]

        group = WordDefinition(dict_parser, sslitem)
        group.build()
        result = group.translate()

        self.assertEqual(result, {"category": "US", "def": "no longer in play (said of a football)"})

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
                "value": "adjective",
                "defs": [
                    {"def": "descending; directed toward a lower position"},
                    {"def": "in a lower place; on the ground"},
                    {"def": "gone, brought, pulled, etc. down"},
                    {"def_subgroup": [
                        {"def": "depressed; dejected"},
                        {"category": "slang", "def": "depressing or downbeat", "example": "a down atmosphere"},
                    ]},
                    {"def": "dejected; discouraged"},
                    {"def": "prostrate; ill"},
                    {"def": "completed; finished", "example": "four down, six to go"},
                    {"def": "inoperative", "example": "the computer is down"},
                    {"def": "characterized by low or falling prices"},
                    {"category": "slang", "def_subgroup": [
                        {"category": "a generalized term of approval meaning variously", "def": "nice, good, excellent, etc."},
                        {"def": "sophisticated, stylish, etc.; cool; hip"},
                    ]},
                    {"category": "sport", "def_subgroup": [
                        {"category": "US", "def": "no longer in play (said of a football)"},
                        {"def": "trailing an opponent by a specified number of points, strokes, etc."},
                        {"category": "US, baseball", "def": "put out"},
                    ]},
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
                "value": "preposition",
                "defs": [
                    {"def": "down or downward, along, through, into, or upon",
                     "example": "down the street, down the chimney, down the river, down the stairs"}
                ]
            }, result)

    def test_fourth_gram_group_returns_full_content(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[3]

        group = GramGroup(dict_parser, gram_group)
        group.build()
        result = group.translate()

        self.assertEqual(
            {
                "value": "transitive verb",
                "defs": [
                    {"def_subgroup": [
                        {"def": "to put, bring, get, throw, or knock down"},
                        {"def": "to defeat, as in a game"},
                    ]},
                    {"def": "to gulp or eat rapidly"}
                ]
            }, result)

    def test_fifth_gram_group_returns_full_content(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[4]

        group = GramGroup(dict_parser, gram_group)
        group.build()
        result = group.translate()

        self.assertEqual(
            {
                "value": "intransitive verb",
                "defs": [
                    {"category": "rare", "def": "to go, come, or get down"}
                ]
            }, result)

    def test_sixth_gram_group_first_def(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[5]
        sslist = dict_parser.get_senselist(gram_group)
        sslitem = dict_parser.get_all_senselist_items(sslist)[0]

        word = WordDefinition(dict_parser, sslitem)
        word.build()
        result = word.translate()
        self.assertEqual(result["def"], "a downward movement or depressed condition; defeat, misfortune, etc. see also "
                                        "ups and downs (def. 1) at up (def. 1)")

    def test_sixth_gram_group_returns_full_content(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]
        gram_group = dict_parser.get_all_grammar_groups(def_group)[5]

        group = GramGroup(dict_parser, gram_group)
        group.build()
        result = group.translate()

        print(result["defs"][0])

        self.assertEqual(
            {
                "value": "noun",
                "defs": [
                    {"def": "a downward movement or depressed condition; defeat, misfortune, etc. see "
                            "also ups and downs (def. 1) at up (def. 1)"},
                    {"category": "US, American football", "def_subgroup": [
                        {"def": "one of four consecutive plays in which a team, in order to keep possession of the "
                                "ball, must either score or advance the ball at least ten yards"},
                        {"def": "the declaring of the ball as down, or no longer in play"},
                    ]},
                    {"category": "slang", "def": "a barbiturate or other depressant drug; downer"}
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
            {"word": "down",
             "related": ['down and out', 'down on', 'down to the ground', 'down with!'],
             "gram_groups": [
                 {
                     "value": "adverb",
                     "defs": [
                         {"def": "from a higher to a lower place; toward the ground"},
                         {
                             "def": "in, on, or to a lower position or level; specif., to a sitting or reclining position"},
                         {"def_subgroup": [
                             {"def": "in or to a place thought of as lower or below; often, specif., southward",
                              "example": "to go down to Florida"},
                             {"def": "out of one's hand", "example": "put it down"}
                         ]},
                         {"def": "below the horizon"},
                         {"def": "from an earlier to a later period or person", "example": "down through the years"},
                         {"def": "into a low or dejected emotional condition"},
                         {"def": "into a low or prostrate physical condition", "example": "to come down with a cold"},
                         {"def": "in or into an inferior position or condition", "example": "held down by harsh laws"},
                         {"def": "to a lower amount, value, or bulk", "example": "to come down in price"},
                         {"def_subgroup": [
                             {"def": "to a less excited or active condition; into a tranquil or quiet state",
                              "example": "to settle down"},
                             {"def": "to a lower volume of sound", "example": "turn down the radio"},
                         ]},
                         {"def": "in a serious or earnest manner", "example": "to get down to work"},
                         {"def": "completely; to the full extent", "example": "loaded down"},
                         {"def": "in cash or when bought",
                          "example": "five dollars down and the remainder in installments"},
                         {"def": "in writing; on record", "example": "take down his name"},
                     ]
                 },
                 {
                     "value": "adjective",
                     "defs": [
                         {"def": "descending; directed toward a lower position"},
                         {"def": "in a lower place; on the ground"},
                         {"def": "gone, brought, pulled, etc. down"},
                         {"def_subgroup": [
                             {"def": "depressed; dejected"},
                             {"category": "slang", "def": "depressing or downbeat", "example": "a down atmosphere"},
                         ]},
                         {"def": "dejected; discouraged"},
                         {"def": "prostrate; ill"},
                         {"def": "completed; finished", "example": "four down, six to go"},
                         {"def": "inoperative", "example": "the computer is down"},
                         {"def": "characterized by low or falling prices"},
                         {"category": "slang", "def_subgroup": [
                             {"category": "a generalized term of approval meaning variously",
                              "def": "nice, good, excellent, etc."},
                             {"def": "sophisticated, stylish, etc.; cool; hip"},
                         ]},
                         {"category": "sport", "def_subgroup": [
                             {"category": "US", "def": "no longer in play (said of a football)"},
                             {"def": "trailing an opponent by a specified number of points, strokes, etc."},
                             {"category": "US, baseball", "def": "put out"},
                         ]},
                     ]
                 },
                 {
                     "value": "preposition",
                     "defs": [
                         {"def": "down or downward, along, through, into, or upon",
                          "example": "down the street, down the chimney, down the river, down the stairs"}
                     ]
                 },
                 {
                     "value": "transitive verb",
                     "defs": [
                         {"def_subgroup": [
                             {"def": "to put, bring, get, throw, or knock down"},
                             {"def": "to defeat, as in a game"},
                         ]},
                         {"def": "to gulp or eat rapidly"}
                     ]
                 },
                 {
                     "value": "intransitive verb",
                     "defs": [
                         {"category": "rare", "def": "to go, come, or get down"}
                     ]
                 },
                 {
                     "value": "noun",
                     "defs": [
                         {"def": "a downward movement or depressed condition; defeat, misfortune, etc. see "
                                 "also ups and downs (def. 1) at up (def. 1)"},
                         {"category": "US, American football", "def_subgroup": [
                             {
                                 "def": "one of four consecutive plays in which a team, in order to keep possession of the "
                                        "ball, must either score or advance the ball at least ten yards"},
                             {"def": "the declaring of the ball as down, or no longer in play"},
                         ]},
                         {"category": "slang", "def": "a barbiturate or other depressant drug; downer"}
                     ]
                 }

            ]}, result)

    def test_second_def_group_returns_full_content(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[1]

        group = DefGroup(dict_parser, def_group)
        group.build()
        result = group.translate()
        self.assertEqual(
            {"word": "down", "gram_groups": [
                {
                    "value": "noun",
                    "defs": [
                        {"def": "soft, fluffy feathers, as the outer covering on young birds or an inner layer of "
                                "feathers on adult birds"},
                        {"def": "soft, fine hair or hairy growth"}
                    ]
                },
            ]}, result)

    def test_third_def_group_returns_full_content(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[2]

        group = DefGroup(dict_parser, def_group)
        group.build()
        result = group.translate()
        self.assertEqual(
            {"word": "down", "gram_groups": [
                {
                    "value": "noun",
                    "defs": [
                        {"def": "an expanse of open, high, grassy land (usually used in pl.)"}
                    ]
                },
            ]}, result)

    def test_fourth_def_group_returns_full_content(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[3]

        group = DefGroup(dict_parser, def_group)
        group.build()
        result = group.translate()
        self.assertEqual(
            {"word": "Down", "gram_groups": [
                {
                    "defs": [
                        {"def": "former county of E Northern Ireland: c. 952 sq mi (2,466 sq km)"},
                        {"def": "district in E Northern Ireland, in the S part of the former county: 249 sq mi "
                                "(645 sq km); pop. 58,000"}
                    ]
                },
            ]}, result)

    def test_fifth_def_group_returns_full_content(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[4]

        group = DefGroup(dict_parser, def_group)
        group.build()
        result = group.translate()
        self.assertEqual(
            {"word": "down-", "gram_groups": [
                {
                    "defs": [
                        {"def": "down", "example": "downhill"}
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
                {"word": "down",
                 "related": ['down and out', 'down on', 'down to the ground', 'down with!'],
                 "gram_groups": [
                     {
                         "value": "adverb",
                         "defs": [
                             {"def": "from a higher to a lower place; toward the ground"},
                             {
                                 "def": "in, on, or to a lower position or level; specif., to a sitting or reclining position"},
                             {"def_subgroup": [
                                 {"def": "in or to a place thought of as lower or below; often, specif., southward",
                                  "example": "to go down to Florida"},
                                 {"def": "out of one's hand", "example": "put it down"}
                             ]},
                             {"def": "below the horizon"},
                             {"def": "from an earlier to a later period or person",
                              "example": "down through the years"},
                             {"def": "into a low or dejected emotional condition"},
                             {"def": "into a low or prostrate physical condition",
                              "example": "to come down with a cold"},
                             {"def": "in or into an inferior position or condition",
                              "example": "held down by harsh laws"},
                             {"def": "to a lower amount, value, or bulk", "example": "to come down in price"},
                             {"def_subgroup": [
                                 {"def": "to a less excited or active condition; into a tranquil or quiet state",
                                  "example": "to settle down"},
                                 {"def": "to a lower volume of sound", "example": "turn down the radio"},
                             ]},
                             {"def": "in a serious or earnest manner", "example": "to get down to work"},
                             {"def": "completely; to the full extent", "example": "loaded down"},
                             {"def": "in cash or when bought",
                              "example": "five dollars down and the remainder in installments"},
                             {"def": "in writing; on record", "example": "take down his name"},
                         ]
                     },
                     {
                         "value": "adjective",
                         "defs": [
                             {"def": "descending; directed toward a lower position"},
                             {"def": "in a lower place; on the ground"},
                             {"def": "gone, brought, pulled, etc. down"},
                             {"def_subgroup": [
                                 {"def": "depressed; dejected"},
                                 {"category": "slang", "def": "depressing or downbeat", "example": "a down atmosphere"},
                             ]},
                             {"def": "dejected; discouraged"},
                             {"def": "prostrate; ill"},
                             {"def": "completed; finished", "example": "four down, six to go"},
                             {"def": "inoperative", "example": "the computer is down"},
                             {"def": "characterized by low or falling prices"},
                             {"category": "slang", "def_subgroup": [
                                 {"category": "a generalized term of approval meaning variously",
                                  "def": "nice, good, excellent, etc."},
                                 {"def": "sophisticated, stylish, etc.; cool; hip"},
                             ]},
                             {"category": "sport", "def_subgroup": [
                                 {"category": "US", "def": "no longer in play (said of a football)"},
                                 {"def": "trailing an opponent by a specified number of points, strokes, etc."},
                                 {"category": "US, baseball", "def": "put out"},
                             ]},
                         ]
                     },
                     {
                         "value": "preposition",
                         "defs": [
                             {"def": "down or downward, along, through, into, or upon",
                              "example": "down the street, down the chimney, down the river, down the stairs"}
                         ]
                     },
                     {
                         "value": "transitive verb",
                         "defs": [
                             {"def_subgroup": [
                                 {"def": "to put, bring, get, throw, or knock down"},
                                 {"def": "to defeat, as in a game"},
                             ]},
                             {"def": "to gulp or eat rapidly"}
                         ]
                     },
                     {
                         "value": "intransitive verb",
                         "defs": [
                             {"category": "rare", "def": "to go, come, or get down"}
                         ]
                     },
                     {
                         "value": "noun",
                         "defs": [
                             {"def": "a downward movement or depressed condition; defeat, misfortune, etc. see "
                                     "also ups and downs (def. 1) at up (def. 1)"},
                             {"category": "US, American football", "def_subgroup": [
                                 {
                                     "def": "one of four consecutive plays in which a team, in order to keep possession of the "
                                            "ball, must either score or advance the ball at least ten yards"},
                                 {"def": "the declaring of the ball as down, or no longer in play"},
                             ]},
                             {"category": "slang", "def": "a barbiturate or other depressant drug; downer"}
                         ]
                     }

                 ]},
                {"word": "down", "gram_groups": [
                    {
                        "value": "noun",
                        "defs": [
                            {"def": "soft, fluffy feathers, as the outer covering on young birds or an inner layer of "
                                    "feathers on adult birds"},
                            {"def": "soft, fine hair or hairy growth"}
                        ]
                    },
                ]},
                {"word": "down", "gram_groups": [
                    {
                        "value": "noun",
                        "defs": [
                            {"def": "an expanse of open, high, grassy land (usually used in pl.)"}
                        ]
                    },
                ]},
                {"word": "Down", "gram_groups": [
                    {
                        "defs": [
                            {"def": "former county of E Northern Ireland: c. 952 sq mi (2,466 sq km)"},
                            {"def": "district in E Northern Ireland, in the S part of the former county: 249 sq mi "
                                    "(645 sq km); pop. 58,000"}
                        ]
                    },
                ]},
                {"word": "down-", "gram_groups": [
                    {
                        "defs": [
                            {"def": "down", "example": "downhill"}
                        ]
                    }
                ]}

            ], result)

    def test_word_returns_nearby_words(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)

        group = NearbyWordsGroup(dict_parser)
        group.build()
        result = group.translate()
        self.assertEqual([
            "Dow", "Dow Jones industrial average", "dowager", "dowager's hump", "Dowden", "dowdy", "dowel", "dower",
            "dowitcher", "Dowland", "down and out", "down at the heel", "Down East", "down in the mouth", "down on",
            "down on one's luck", "down payment", "down quark", "Down syndrome", "down the drain"], result)

    def test_word_returns_related_defgroup_1(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]

        group = RelatedGroup(dict_parser, def_group)
        group.build()
        result = group.translate()
        self.assertEqual(['down and out', 'down on', 'down to the ground', 'down with!'], result)

    def test_get_translations_to_json(self):
        obj = HtmlToJson(self.word_name, self.html_content)
        json_obj = obj.translate()

        self.assertEqual(json_obj["translations"],
            ["Down means at or to a lower level or position.A man came down the stairs to meet them.",
             "If you say that someone downs food or a drink, you mean that they eat or drink it.We downed bottles of local wine.",
             "Down consists of the small, soft feathers on young birds. Down is used to make bed-covers and pillows.... goose down."])

    def test_translate_html_to_json(self):
        obj = HtmlToJson(self.word_name, self.html_content)
        json_str = obj.translate()

        self.assertEqual(json_str,
        {
            "frequency": "Extremely Common",
            "def_groups": [
                {"word": "down",
                 "related": ['down and out', 'down on', 'down to the ground', 'down with!'],
                 "gram_groups": [
                     {
                         "value": "adverb",
                         "defs": [
                             {"def": "from a higher to a lower place; toward the ground"},
                             {
                                 "def": "in, on, or to a lower position or level; specif., to a sitting or reclining position"},
                             {"def_subgroup": [
                                 {"def": "in or to a place thought of as lower or below; often, specif., southward",
                                  "example": "to go down to Florida"},
                                 {"def": "out of one's hand", "example": "put it down"}
                             ]},
                             {"def": "below the horizon"},
                             {"def": "from an earlier to a later period or person",
                              "example": "down through the years"},
                             {"def": "into a low or dejected emotional condition"},
                             {"def": "into a low or prostrate physical condition",
                              "example": "to come down with a cold"},
                             {"def": "in or into an inferior position or condition",
                              "example": "held down by harsh laws"},
                             {"def": "to a lower amount, value, or bulk", "example": "to come down in price"},
                             {"def_subgroup": [
                                 {"def": "to a less excited or active condition; into a tranquil or quiet state",
                                  "example": "to settle down"},
                                 {"def": "to a lower volume of sound", "example": "turn down the radio"},
                             ]},
                             {"def": "in a serious or earnest manner", "example": "to get down to work"},
                             {"def": "completely; to the full extent", "example": "loaded down"},
                             {"def": "in cash or when bought",
                              "example": "five dollars down and the remainder in installments"},
                             {"def": "in writing; on record", "example": "take down his name"},
                         ]
                     },
                     {
                         "value": "adjective",
                         "defs": [
                             {"def": "descending; directed toward a lower position"},
                             {"def": "in a lower place; on the ground"},
                             {"def": "gone, brought, pulled, etc. down"},
                             {"def_subgroup": [
                                 {"def": "depressed; dejected"},
                                 {"category": "slang", "def": "depressing or downbeat", "example": "a down atmosphere"},
                             ]},
                             {"def": "dejected; discouraged"},
                             {"def": "prostrate; ill"},
                             {"def": "completed; finished", "example": "four down, six to go"},
                             {"def": "inoperative", "example": "the computer is down"},
                             {"def": "characterized by low or falling prices"},
                             {"category": "slang", "def_subgroup": [
                                 {"category": "a generalized term of approval meaning variously",
                                  "def": "nice, good, excellent, etc."},
                                 {"def": "sophisticated, stylish, etc.; cool; hip"},
                             ]},
                             {"category": "sport", "def_subgroup": [
                                 {"category": "US", "def": "no longer in play (said of a football)"},
                                 {"def": "trailing an opponent by a specified number of points, strokes, etc."},
                                 {"category": "US, baseball", "def": "put out"},
                             ]},
                         ]
                     },
                     {
                         "value": "preposition",
                         "defs": [
                             {"def": "down or downward, along, through, into, or upon",
                              "example": "down the street, down the chimney, down the river, down the stairs"}
                         ]
                     },
                     {
                         "value": "transitive verb",
                         "defs": [
                             {"def_subgroup": [
                                 {"def": "to put, bring, get, throw, or knock down"},
                                 {"def": "to defeat, as in a game"},
                             ]},
                             {"def": "to gulp or eat rapidly"}
                         ]
                     },
                     {
                         "value": "intransitive verb",
                         "defs": [
                             {"category": "rare", "def": "to go, come, or get down"}
                         ]
                     },
                     {
                         "value": "noun",
                         "defs": [
                             {"def": "a downward movement or depressed condition; defeat, misfortune, etc. see "
                                     "also ups and downs (def. 1) at up (def. 1)"},
                             {"category": "US, American football", "def_subgroup": [
                                 {
                                     "def": "one of four consecutive plays in which a team, in order to keep possession of the "
                                            "ball, must either score or advance the ball at least ten yards"},
                                 {"def": "the declaring of the ball as down, or no longer in play"},
                             ]},
                             {"category": "slang", "def": "a barbiturate or other depressant drug; downer"}
                         ]
                     }

                 ]},
                {"word": "down", "gram_groups": [
                    {
                        "value": "noun",
                        "defs": [
                            {"def": "soft, fluffy feathers, as the outer covering on young birds or an inner layer of "
                                    "feathers on adult birds"},
                            {"def": "soft, fine hair or hairy growth"}
                        ]
                    },
                ]},
                {"word": "down", "gram_groups": [
                    {
                        "value": "noun",
                        "defs": [
                            {"def": "an expanse of open, high, grassy land (usually used in pl.)"}
                        ]
                    },
                ]},
                {"word": "Down", "gram_groups": [
                    {
                        "defs": [
                            {"def": "former county of E Northern Ireland: c. 952 sq mi (2,466 sq km)"},
                            {"def": "district in E Northern Ireland, in the S part of the former county: 249 sq mi "
                                    "(645 sq km); pop. 58,000"}
                        ]
                    },
                ]},
                {"word": "down-", "gram_groups": [
                    {
                        "defs": [
                            {"def": "down", "example": "downhill"}
                        ]
                    }
                ]}
            ],
            "examples": [],
            "nearby_words": [
                "Dow", "Dow Jones industrial average", "dowager", "dowager's hump", "Dowden", "dowdy", "dowel", "dower",
                "dowitcher", "Dowland", "down and out", "down at the heel", "Down East", "down in the mouth", "down on",
                "down on one's luck", "down payment", "down quark", "Down syndrome", "down the drain"
            ],
            "translations": [
                "Down means at or to a lower level or position.A man came down the stairs to meet them.",
                "If you say that someone downs food or a drink, you mean that they eat or drink it.We downed bottles of local wine.",
                "Down consists of the small, soft feathers on young birds. Down is used to make bed-covers and pillows.... goose down."
            ]
        })

if __name__ == '__main__':
    unittest.main()
