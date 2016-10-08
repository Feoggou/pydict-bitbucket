import unittest
import os
from unittest.mock import patch
from src.def_groups import *
from src.def_parser import DefParser
from lxml import etree

from src.html_parser import HtmlParser
from src import config


class HtmlToJsonTest(unittest.TestCase):
    word_name = ""
    html_content = ""

    @classmethod
    def setUpClass(cls):
        file_name = os.path.join(config.HTML_SOURCE_PATH, "soliloquy_defs.html")

        with open(file_name) as f:
            cls.word_name = "soliloquy"
            cls.html_content = f.read()

    def test_usage_note(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)
        etree_group = dict_parser.get_all_def_groups()[0]

        def_group = DefGroup(dict_parser, etree_group)
        def_group.build()
        result = def_group.translate()

        self.assertEqual("Soliloquy is sometimes wrongly used where monologue is meant. Both words refer to a long "
                         "speech by one person, but a monologue can be addressed to other people, whereas in a "
                         "soliloquy the speaker is always talking to himself or herself",
                         result["note"])


if __name__ == '__main__':
    unittest.main()
