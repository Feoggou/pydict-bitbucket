import unittest
from src.html_to_json import HtmlToJson, HtmlToJsonRelated, HtmlToJsonSynonyms


class HtmlToJsonTest(unittest.TestCase):

    def setUp(self):
        f = open("do_defs.html")
        self.word_name = "do"

        self.html_content = f.read()
        # self.maxDiff = None

        f = open("do_syn.html")
        self.syn_content = f.read()

        f = open("do_related.html")
        self.related_content = f.read()

    def test_translate_html_syn_rel_to_json(self):
        obj = HtmlToJson(self.word_name, self.html_content)
        do_word = obj.translate()

        synonyms = HtmlToJsonSynonyms(self.word_name, self.syn_content)
        do_word["synonyms"] = synonyms.translate()

        related = HtmlToJsonRelated(self.related_content)
        do_word["related_words"] = related.translate()

        self.assertEqual(do_word,
        {
            "frequency": "Extremely Common",
            "def_groups": [
                {"word": "do",
                 "related": [
                     "do a deal", "do by", "do down", "do in", "do it", "do over", "do's and don'ts",
                     "do up", "do up right", "do oneself well", "do with", "do without", "have to do with"
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
                            {"def": "to finish (used in the perfect tense [have done with dreaming ])"},
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
                        "defs": [
                            {"category": "music", "def": "a syllable representing the first or last tone of the diatonic scale"}
                        ]
                    },
                ]},
                {"word": "do", "gram_groups": [
                    {
                        "value": "noun",
                        "defs": [
                            {"category": "slang", "def": "hairdo"}
                        ]
                    },
                ]},
                {"word": "Do or do", "gram_groups": [
                    {
                        "defs": [
                            {"def": "ditto"}
                        ]
                    },
                ]},
                {"word": "DO or D.O.", "gram_groups": [
                    {
                        "defs": [
                            {"def": "Doctor of Osteopathy"}
                        ]
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
            ],
            "synonyms": [
                {"word": "do", "gram_groups": [
                    {"gram_group": {
                        "value": "verb",
                        "synonyms": [
                            {"line": ["perform", "accomplish", "achieve", "carry out", "complete", "execute"]},
                            {"line": ["be adequate", "be sufficient", "cut the mustard", "pass muster", "satisfy", "suffice"]},
                            {"line": ["get ready", "arrange", "fix", "look after", "prepare", "see to"]},
                            {"line": ["solve", "decipher", "decode", "figure out", "puzzle out", "resolve", "work out"]},
                            {"line": ["cause", "bring about", "create", "effect", "produce"]}
                        ]
                    }},
                    {"gram_group": {
                        "value": "noun",
                        "synonyms": [
                            {"category": "informal mainly British New Zealand",
                             "line": ["event", "affair", "function", "gathering", "occasion", "party"]},
                        ]
                    }}
                ]}
            ],
            "related_words": [
                "do by", "do up", "do down", "do time", "make do", "do-gooder", "do penance", "do-or-die", "do honor to",
                "do up right", "whoop-de-do", "do credit to", "do the honors", "do oneself well", "do-it-yourself",
                "do one's (or its) business", "have to do with", "Mato Grosso do Sul", "do in", "to-do", "do gree",
                "do with", "do-si-do", "derring-do", "do without", "how-do-you-do", "do to death", "tae kwon do",
                "How do you do?", "do justice to", "do the trick", "do someone dirt", "do a number on", "do oneself justice",
                "do one's damnedest (or damndest)", "Rio Grande do Norte", "do it", "can-do", "do over", "do-rag",
                "do tell!", "do a deal", "do-nothing", "do duty for", "do up brown", "well-to-do", "do away with",
                "do one's bit", "ne'er-do-well", "do wonders for", "do business with", "do oneself proud",
                "do the bidding of", "Rio Grande do Sul"
            ],
            "translations": [
                "When you do something, you take some action or perform an activity or task.I was trying to do some work. done"
            ]
        })

if __name__ == '__main__':
    unittest.main()
