import unittest
import os

from lxml import etree

from src.def_parser import DefParser
from src import config


class TestParser(unittest.TestCase):
    root = None

    @classmethod
    def setUpClass(cls):
        file_name = os.path.join(config.HTML_SOURCE_PATH, "lead_defs.html")

        with open(file_name) as f:
            text = f.read()

        TestParser.root = etree.HTML(text)

    def setUp(self):
        self.parser = DefParser(TestParser.root, "lead")

    def test_getMultipleTranslations(self):
        translations = self.parser.get_all_translations()

        self.assertEqual([
            {
                "def": "Lead is a soft, grey, heavy metal.",
                "category": "metal",
                "example": "",
                "value": "noun",
                "word": "lead"
            },
            {
                "def": "The lead in a play, film, or show is the most important role in it.",
                "category": "in a play or film",
                "example": "She recently played the lead in a film.",
                "value": "noun",
                "word": "lead"
            },
            {
                "def": "If you are in the lead in a race or competition, you are winning.",
                "category": "in a race or competition",
                "example": "Our team was in the lead after ten minutes.",
                "value": "noun",
                "word": "lead"
            },
            {
                "def": "If you lead someone to a place, you take them there.",
                "category": "",
                "example": "I took his hand and started to lead him into the house.",
                "value": "verb",
                "word": "lead"
            },
        ],
                         translations)


if __name__ == '__main__':
    unittest.main()
