import unittest
from src.html_parser.syn_groups import *


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
                            "line": [{"syn": "swindle"}, {"syn": "deception"}, {"syn": "fraud"},
                                     {"syn": "scam", "category": "slang"}, {"syn": "sting", "category": "informal"},
                                     {"syn": "trick"}]
                        },
                    ]
                }},
                {"gram_group": {
                    "value": "verb",
                    "synonyms": [
                        {
                            "line": [
                                {"syn": "swindle"}, {"syn": "cheat"}, {"syn": "deceive"}, {"syn": "defraud"},
                                {"syn": "double-cross", "category": "informal"}, {"syn": "dupe"}, {"syn": "hoodwink"},
                                {"syn": "rip off", "category": "slang"}, {"syn": "trick"}]}
                    ]
                }}
            ]}
        ])

if __name__ == '__main__':
    unittest.main()
