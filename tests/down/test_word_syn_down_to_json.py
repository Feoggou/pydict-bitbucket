import unittest
from src.syn_groups import *
from src.syn_parser import SynParser
from lxml import etree


class HtmlToJsonSynTest(unittest.TestCase):
    def setUp(self):
        f = open("down_syn.html")
        self.word_name = "down"
        self.html_content = f.read()
        self.maxDiff = None

    def test_create_html_to_json_obj(self):
        obj = HtmlToJsonSynonyms(self.word_name, self.html_content)
        self.assertIsNotNone(obj)

    def test_return_all(self):
        obj = HtmlToJsonSynonyms(self.word_name, self.html_content)

        json_obj = obj.translate()

        self.assertEqual(json_obj, [
            {"word": "down", "gram_groups": [
                {"gram_group": {
                    "value": "adjective",
                    "synonyms": [
                        {"line": ["depressed", "dejected", "disheartened", "downcast", "low", "miserable", "sad", "unhappy"]}
                    ]
                }},
                {"gram_group": {
                    "value": "verb",
                    "synonyms": [
                        {"category": "informal",
                         "line": [
                             "swallow", "drain", "drink", "drink down", "gulp", "put away", "toss off"]
                         },
                    ]
                }},
                {"gram_group": {
                    "value": "noun",
                    "synonyms": [
                        {"line": [
                             "See have a down on"]
                         },
                    ]
                }}
            ]}
        ])

if __name__ == '__main__':
    unittest.main()
