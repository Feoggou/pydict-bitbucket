import unittest
from src.syn_groups import *
from src.syn_parser import SynParser
from lxml import etree


class HtmlToJsonSynTest(unittest.TestCase):
    def setUp(self):
        f = open("measly_syn.html")
        self.word_name = "measly"
        self.html_content = f.read()
        self.maxDiff = None

    def test_create_html_to_json_obj(self):
        obj = HtmlToJsonSynonyms(self.word_name, self.html_content)
        self.assertIsNotNone(obj)

    def test_return_all(self):
        obj = HtmlToJsonSynonyms(self.word_name, self.html_content)

        json_obj = obj.translate()
        self.assertEqual(json_obj, [
            {"word": "measly", "gram_groups": [
                {"gram_group": {
                    "value": "adjective",
                    "synonyms": [
                        {"line": ["meager", "miserable", "paltry", "pathetic", "pitiful", "poor", "puny", "scanty", "skimpy"]}
                    ]
                }},
            ]}
        ])

if __name__ == '__main__':
    unittest.main()
