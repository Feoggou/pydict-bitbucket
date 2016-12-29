import os

import unittest

from src.json_reader import DefGroupReader
from src import config


class JsonReaderTest(unittest.TestCase):
    tests_path = None

    @classmethod
    def setUpClass(cls):
        config.USE_COLORS = False
        cls.tests_path = os.path.dirname(os.path.abspath(__file__))

    def test_json_soliloquy_has_usage(self):
        json_obj = {
            "gram_groups": [],
            "note": "Soliloquy is sometimes wrongly used where monologue is meant. Both words refer to a long "
                    "speech by one person, but a monologue can be addressed to other people, whereas in a "
                    "soliloquy the speaker is always talking to himself or herself",
        }

        reader = DefGroupReader(dict())
        result = reader.read_def_group(json_obj)

        self.assertEqual("NOTE\nSoliloquy is sometimes wrongly used where monologue is meant. Both words refer to a "
                         "long speech by one person, but a monologue can be addressed to other people, whereas in a "
                         "soliloquy the speaker is always talking to himself or herself\n\n", result)


if __name__ == '__main__':
    unittest.main()
