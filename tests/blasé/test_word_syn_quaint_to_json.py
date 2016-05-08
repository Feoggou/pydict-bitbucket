import unittest
# import json

from src.html_parser.syn_groups import *


class HtmlToJsonSynTest(unittest.TestCase):
    def setUp(self):
        f = open("quaint_syn.html")
        self.word_name = "quaint"
        self.html_content = f.read()
        self.maxDiff = None

    def test_create_html_to_json_obj(self):
        obj = HtmlToJsonSynonyms(self.word_name, self.html_content)
        self.assertIsNotNone(obj)

    def test_return_all(self):
        obj = HtmlToJsonSynonyms(self.word_name, self.html_content)

        json_obj = obj.translate()
        # print(json.dumps(json_obj, indent=4, sort_keys=True))

        self.assertEqual(json_obj, [
            {"word": "quaint", "gram_groups": [
                {"gram_group": {
                    "value": "adjective",
                    "synonyms": [
                        {"line": [{"syn": "unusual"}, {"syn": "bizarre"}, {"syn": "curious"}, {"syn": "droll"},
                                  {"syn": "eccentric"}, {"syn": "fanciful"}, {"syn": "odd"}, {"syn": "old-fashioned"},
                                  {"syn": "peculiar"}, {"syn": "queer"}, {"syn": "rum", "category": "British, slang"},
                                  {"syn": "singular"}, {"syn": "strange"}]},
                        {"line": [{"syn": "old-fashioned"}, {"syn": "antiquated"}, {"syn": "old-world"},
                                  {"syn": "picturesque"}]},
                    ]
                }},
            ]}
        ])

if __name__ == '__main__':
    unittest.main()
