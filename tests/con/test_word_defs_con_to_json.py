import unittest
from unittest.mock import patch
from src.html_parser.def_groups import *
from src.html_parser.def_parser import DefParser
from lxml import etree


class HtmlToJsonTest(unittest.TestCase):

    def setUp(self):
        f = open("con_defs.html")
        self.word_name = "con"

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
        self.assertEqual(result, "Very Common")

    # word / def_groups
    def test_def_groups_returns_7_def_groups(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)

        with patch.object(DefGroup, 'build'):
            group = DefGroups(dict_parser)
            group.build()
            result = group.translate()
            print(result)
            self.assertEqual([
                {"word": "con", "gram_groups": []}, {"word": "con", "gram_groups": []},
                {"word": "con", "gram_groups": []}, {"word": "con", "gram_groups": []},
                {"word": "con", "gram_groups": []}, {"word": "con", "gram_groups": []},
                {"word": "con-", "gram_groups": []},
            ], result)

    # word / def_groups / def_group [0] / gram_groups
    def test_first_def_group_returns_3_gram_groups(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[0]

        with patch.object(GramGroup, 'build'):
            with patch.object(RelatedGroup, 'build'):
                group = DefGroup(dict_parser, def_group)
                group.build()
                result = group.translate()
                self.assertEqual({"word": "con", "gram_groups": [{}, {}, {}]},
                                 result)

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
        self.assertEqual({"category": "slang", "def": "confidence (def. 1)", "example": "a con man"}, result)

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
            {"category": "slang", "def": "confidence (def. 1)", "example": "a con man"}
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
                    {"category": "slang", "def": "confidence (def. 1)", "example": "a con man"}
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
                "word_forms": ["conned", "conning"],
                "defs": [
                    {"def": "to swindle (a victim) by first gaining the person's confidence"},
                    {"def": "to trick or fool, esp. by glib persuasion"},
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
                    {"category": "slang", "def": "the act or an instance of conning; swindle; trick"},
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
            {"word": "con",
             "gram_groups": [
                 {
                     "value": "adjective",
                     "defs": [
                         {"category": "slang", "def": "confidence (def. 1)", "example": "a con man"}
                     ]
                 },
                 {
                     "value": "transitive verb",
                     "word_forms": ["conned", "conning"],
                     "defs": [
                         {"def": "to swindle (a victim) by first gaining the person's confidence"},
                         {"def": "to trick or fool, esp. by glib persuasion"},
                     ]
                 },
                 {
                     "value": "noun",
                     "defs": [
                         {"category": "slang", "def": "the act or an instance of conning; swindle; trick"},
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
        # print(result)

        self.assertEqual(
            {"word": "con", "gram_groups": [
                {
                    "value": "adverb",
                    "defs": [
                        {"def": "against; in opposition", "example": "to argue a matter pro and con"}
                    ]
                },
                {
                    "value": "noun",
                    "defs": [
                        {"def": "a reason, vote, position, etc. in opposition"}
                    ]
                }
            ]}, result)

    def test_third_def_group_returns_full_content(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[2]

        group = DefGroup(dict_parser, def_group)
        group.build()
        result = group.translate()
        self.assertEqual(
            {"word": "con", "gram_groups": [
                {
                    "value": "transitive verb",
                    "word_forms": ["conned", "conning"],
                    "defs": [
                        {"def": "to peruse carefully; study; fix in the memory"}
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
            {"word": "con", "gram_groups": [
                {
                    "value": "transitive verb noun",
                    "word_forms": ["conned", "conning"],
                    "defs": [
                        {"def": "conn (def. 1)"}
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
            {"word": "con", "gram_groups": [
                {
                    "value": "noun",
                    "defs": [
                        {"category": "slang", "def": "convict (def. 1)"}
                    ]
                }
            ]}, result)

    def test_sixth_def_group_returns_full_content(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[5]

        group = DefGroup(dict_parser, def_group)
        group.build()
        result = group.translate()
        self.assertEqual(
            {"word": "con", "gram_groups": [
                {
                    "defs": [
                        {"def": "consolidated"},
                        {"def": "consul"},
                        {"def": "continued"}
                    ]
                }
            ]}, result)

    def test_seventh_def_group_returns_full_content(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        def_group = dict_parser.get_all_def_groups()[6]

        group = DefGroup(dict_parser, def_group)
        group.build()
        result = group.translate()
        print(result)
        self.assertEqual(
            {"word": "con-", "gram_groups": [
                {
                    "defs": [
                        {"def": "(used before c, d, g, j, n, q, s, t, v, and sometimes f) com- (def. 1)",
                         "example": "condominium, confrere"}
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
                {"word": "con",
                 "gram_groups": [
                     {
                         "value": "adjective",
                         "defs": [
                             {"category": "slang", "def": "confidence (def. 1)", "example": "a con man"}
                         ]
                     },
                     {
                         "value": "transitive verb",
                         "word_forms": ["conned", "conning"],
                         "defs": [
                             {"def": "to swindle (a victim) by first gaining the person's confidence"},
                             {"def": "to trick or fool, esp. by glib persuasion"},
                         ]
                     },
                     {
                         "value": "noun",
                         "defs": [
                             {"category": "slang", "def": "the act or an instance of conning; swindle; trick"},
                         ]
                     }

                 ]},
                {"word": "con", "gram_groups": [
                    {
                        "value": "adverb",
                        "defs": [
                            {"def": "against; in opposition", "example": "to argue a matter pro and con"}
                        ]
                    },
                    {
                        "value": "noun",
                        "defs": [
                            {"def": "a reason, vote, position, etc. in opposition"}
                        ]
                    }
                ]},
                {"word": "con", "gram_groups": [
                    {
                        "value": "transitive verb",
                        "word_forms": ["conned", "conning"],
                        "defs": [
                            {"def": "to peruse carefully; study; fix in the memory"}
                        ]
                    },
                ]},
                {"word": "con", "gram_groups": [
                    {
                        "value": "transitive verb noun",
                        "word_forms": ["conned", "conning"],
                        "defs": [
                            {"def": "conn (def. 1)"}
                        ]
                    },
                ]},
                {"word": "con", "gram_groups": [
                    {
                        "value": "noun",
                        "defs": [
                            {"category": "slang", "def": "convict (def. 1)"}
                        ]
                    }
                ]},
                {"word": "con", "gram_groups": [
                    {
                        "defs": [
                            {"def": "consolidated"},
                            {"def": "consul"},
                            {"def": "continued"}
                        ]
                    }
                ]},
                {"word": "con-", "gram_groups": [
                    {
                        "defs": [
                            {"def": "(used before c, d, g, j, n, q, s, t, v, and sometimes f) com- (def. 1)",
                             "example": "condominium, confrere"}
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
                {"example": "I ain't in Brooklyn now, I didn't happen to con nobody out of the number for this particular phone."}
            ], result)

    def test_word_returns_nearby_words(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)

        group = NearbyWordsGroup(dict_parser)
        group.build()
        result = group.translate()
        self.assertEqual([
            "Comr", "comrade", "comrade in arms", "comradery", "Comsat", "Comstock Lode", "Comstockery", "comte",
            "comtesse", "Comus", "con amore", "con brio", "con dolore", "con man", "con moto", "con spirito",
            "con-", "Conakry", "Conan Doyle", "Conant"
        ], result)

    def test_get_translations_to_json(self):
        obj = HtmlToJson(self.word_name, self.html_content)
        json_obj = obj.translate()

        self.assertEqual(json_obj["translations"], [
            "If someone cons you, they persuade you to do something or believe something by telling you things that "
            "are not true. conned, conning, cons --- He claimed that the businessman had conned him out of a lot of money.",
            "A con is a trick in which someone deceives you by telling you something that is not true. cons --- Snacks "
            "that offer miraculous weight loss are a con."
        ])

    def test_translate_html_to_json(self):
        obj = HtmlToJson(self.word_name, self.html_content)
        json_str = obj.translate()

        self.assertEqual(json_str,
        {
            "frequency": "Very Common",
            "def_groups": [
                {"word": "con",
                 "gram_groups": [
                     {
                         "value": "adjective",
                         "defs": [
                             {"category": "slang", "def": "confidence (def. 1)", "example": "a con man"}
                         ]
                     },
                     {
                         "value": "transitive verb",
                         "word_forms": ["conned", "conning"],
                         "defs": [
                             {"def": "to swindle (a victim) by first gaining the person's confidence"},
                             {"def": "to trick or fool, esp. by glib persuasion"},
                         ]
                     },
                     {
                         "value": "noun",
                         "defs": [
                             {"category": "slang", "def": "the act or an instance of conning; swindle; trick"},
                         ]
                     }

                 ]},
                {"word": "con", "gram_groups": [
                    {
                        "value": "adverb",
                        "defs": [
                            {"def": "against; in opposition", "example": "to argue a matter pro and con"}
                        ]
                    },
                    {
                        "value": "noun",
                        "defs": [
                            {"def": "a reason, vote, position, etc. in opposition"}
                        ]
                    }
                ]},
                {"word": "con", "gram_groups": [
                    {
                        "value": "transitive verb",
                        "word_forms": ["conned", "conning"],
                        "defs": [
                            {"def": "to peruse carefully; study; fix in the memory"}
                        ]
                    },
                ]},
                {"word": "con", "gram_groups": [
                    {
                        "value": "transitive verb noun",
                        "word_forms": ["conned", "conning"],
                        "defs": [
                            {"def": "conn (def. 1)"}
                        ]
                    },
                ]},
                {"word": "con", "gram_groups": [
                    {
                        "value": "noun",
                        "defs": [
                            {"category": "slang", "def": "convict (def. 1)"}
                        ]
                    }
                ]},
                {"word": "con", "gram_groups": [
                    {
                        "defs": [
                            {"def": "consolidated"},
                            {"def": "consul"},
                            {"def": "continued"}
                        ]
                    }
                ]},
                {"word": "con-", "gram_groups": [
                    {
                        "defs": [
                            {"def": "(used before c, d, g, j, n, q, s, t, v, and sometimes f) com- (def. 1)",
                             "example": "condominium, confrere"}
                        ]
                    }
                ]}
            ],
            "examples": [
                {"example": "I ain't in Brooklyn now, I didn't happen to con nobody out of the number for this particular phone."}
            ],
            "nearby_words": [
                "Comr", "comrade", "comrade in arms", "comradery", "Comsat", "Comstock Lode", "Comstockery", "comte",
                "comtesse", "Comus", "con amore", "con brio", "con dolore", "con man", "con moto", "con spirito",
                "con-", "Conakry", "Conan Doyle", "Conant"
            ],
            "translations": [
                "If someone cons you, they persuade you to do something or believe something by telling you things that "
                "are not true. conned, conning, cons --- He claimed that the businessman had conned him out of a lot of money.",
                "A con is a trick in which someone deceives you by telling you something that is not true. cons --- Snacks "
                "that offer miraculous weight loss are a con."
            ]
        })

if __name__ == '__main__':
    unittest.main()
