import unittest
# import json

from src.html_parser.syn_groups import *


class HtmlToJsonSynTest(unittest.TestCase):
    def setUp(self):
        f = open("scoff_syn.html")
        self.word_name = "scoff"
        self.html_content = f.read()
        self.maxDiff = None

    def test_create_html_to_json_obj(self):
        obj = HtmlToJsonSynonyms(self.word_name, self.html_content)
        self.assertIsNotNone(obj)

    def test_return_all(self):
        obj = HtmlToJsonSynonyms(self.word_name, self.html_content)

        json_obj = obj.translate()
        # print(json.dumps(json_obj, indent=4, sort_keys=True))

        self.assertEqual(json_obj, [{
            "gram_groups": [{
                "gram_group": {
                    "synonyms": [{
                        "line": [
                            {"syn": "scorn"},
                            {"syn": "belittle"},
                            {"syn": "deride"},
                            {"syn": "despise"},
                            {"syn": "jeer"},
                            {"category": "informal", "syn": "knock"},
                            {"syn": "laugh at"},
                            {"syn": "mock"},
                            {"syn": "pooh-pooh"},
                            {"syn": "ridicule"},
                            {"syn": "sneer"}
                        ]
                    }],
                    "value": "verb"
                }
            }],
            "word": "scoff"
        }, {
            "gram_groups": [{
                "gram_group": {
                    "synonyms": [{
                        "line": [
                            {"syn": "gobble"},
                            {"syn": "gobble up"},
                            {"syn": "bolt"},
                            {"syn": "devour"},
                            {"syn": "gorge oneself on"},
                            {"syn": "gulp down"},
                            {"syn": "guzzle"},
                            {"syn": "wolf"}
                        ]
                    }],
                    "value": "verb"
                }
            }],
            "word": "scoff"
        }]
    )

if __name__ == '__main__':
    unittest.main()
