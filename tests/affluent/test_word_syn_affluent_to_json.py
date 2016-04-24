import unittest
from src.html_parser.syn_groups import *


class HtmlToJsonSynTest(unittest.TestCase):
    def setUp(self):
        f = open("affluent_syn.html")
        self.word_name = "affluent"
        self.html_content = f.read()
        self.maxDiff = None

    def test_create_html_to_json_obj(self):
        obj = HtmlToJsonSynonyms(self.word_name, self.html_content)
        self.assertIsNotNone(obj)

    def test_return_all(self):
        obj = HtmlToJsonSynonyms(self.word_name, self.html_content)

        json_obj = obj.translate()
        self.assertEqual(json_obj, [
            {"word": "affluent", "gram_groups": [
                {"gram_group": {
                    "value": "adjective",
                    "synonyms": [
                        {
                            "category": "slang informal",
                            "line": [
                                "wealthy", "loaded", "moneyed", "opulent", "prosperous", "rich",
                                "well-heeled", "well-off", "well-to-do"
                        ]},
                    ]
                }},
            ]}
        ])

if __name__ == '__main__':
    unittest.main()
