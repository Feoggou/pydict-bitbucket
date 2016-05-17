import unittest
# import json

from src.html_parser.syn_groups import *


class HtmlToJsonSynTest(unittest.TestCase):
    def setUp(self):
        with open("blase_syn.html") as f:
            self.html_content = f.read()

        self.word_name = "blasé"
        self.maxDiff = None

    def test_create_html_to_json_obj(self):
        obj = HtmlToJsonSynonyms(self.word_name, self.html_content)
        self.assertIsNotNone(obj)

    def test_return_all(self):
        obj = HtmlToJsonSynonyms(self.word_name, self.html_content)

        json_obj = obj.translate()
        # print(json.dumps(json_obj, indent=4, sort_keys=True))

        self.assertEqual(json_obj, [
            {"word": "blasé", "gram_groups": [
                {"gram_group": {
                    "value": "adjective",
                    "synonyms": [
                        {"line": [{"syn": "indifferent"}, {"syn": "apathetic"}, {"syn": "lukewarm"}, {"syn": "nonchalant"},
                                  {"syn": "offhand"}, {"syn": "unconcerned"}]},
                    ]
                }},
            ]}
        ])

if __name__ == '__main__':
    unittest.main()
