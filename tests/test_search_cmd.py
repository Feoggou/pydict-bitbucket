import unittest
from unittest.mock import patch

from src import commands
from src.cmd_search import SearchCommand
from src.colors import *
from src.json_seeker import *


class TestSearchCommand(unittest.TestCase):
    def setUp(self):
        self.dir_path = "./search-tests-data"

    def test_command_defs_returns_SearchCmd_class(self):
        input_str = "search(do)"

        command = commands.match_command(input_str)
        self.assertIsInstance(command, SearchCommand)

    def test_find_play_inDirectory(self):
        cmd = SearchCommand("play")
        cmd.set_dir_path(self.dir_path)

        # must: 1. search the directory for all files.
        #       2. retrieve the path to each file.
        #       3. for each file, do a search content on the json file.
        #       4. retrieve content for each file.
        #       5. process content: sorted, unique
        #       6. output process: an object that can be __str__-ed.

        results = cmd.execute().items

        self.assertEqual(results, {
            "synonyms": [
                {
                    'perform.json': [
                        'play'
                    ]
                },
            ],
            "definitions": [
                {
                    "do.json": [
                        "to produce or appear in (a play, etc.)",
                        "to play the role of"
                    ]
                },
                {
                    "perform.json": [
                        "to carry out or execute an action or process; esp., to take part in a musical program, "
                        "act in a play, dance, etc. before an audience"
                    ]
                },
                {
                    "create.json": [
                        "to be the first to portray (a particular role in a play)"
                    ]
                }
            ]
        })


if __name__ == '__main__':
    unittest.main()
