import unittest
from src.syn_groups import *
from src.syn_parser import SynParser
from lxml import etree


class HtmlToJsonSynTest(unittest.TestCase):
    def setUp(self):
        f = open("con_syn.html")
        self.word_name = "con"
        self.html_content = f.read()
        self.maxDiff = None

    def test_create_html_to_json_obj(self):
        obj = HtmlToJsonSynonyms(self.word_name, self.html_content)
        self.assertIsNotNone(obj)

    def test_return_all(self):
        obj = HtmlToJsonSynonyms(self.word_name, self.html_content)

        json_obj = obj.translate()

        self.assertEqual(json_obj, [
            {"word": "con (informal)", "gram_groups": [
                {"gram_group": {
                    "value": "noun",
                    "synonyms": [
                        {
                            "category": "slang informal",
                            "line": ["swindle", "deception", "fraud", "scam", "sting", "trick"]
                        },
                    ]
                }},
                {"gram_group": {
                    "value": "verb",
                    "synonyms": [
                        {"category": "informal slang",
                         "line": [
                             "swindle", "cheat", "deceive", "defraud", "double-cross", "dupe", "hoodwink",
                             "rip off", "trick"]}
                    ]
                }}
            ]}
        ])

if __name__ == '__main__':
    unittest.main()
