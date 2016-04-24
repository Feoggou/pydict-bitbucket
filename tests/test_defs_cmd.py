import unittest
from unittest.mock import patch

from src.cmds import commands
from src.cmds.cmd_defs import DefsCommand
from src.colors import *
from src.json.json_seeker import *


class TestDefsCommand(unittest.TestCase):
    def setUp(self):
        self.dir_path = "./search-tests-data"

    def test_command_defs_returns_DefsCmd_class(self):
        input_str = "defs(do)"

        command = commands.match_command(input_str)
        self.assertIsInstance(command, DefsCommand)

    def test_find_play_inDirectory(self):
        cmd = DefsCommand("play")
        cmd.set_dir_path(self.dir_path)

        # must: 1. search the directory for all files.
        #       2. retrieve the path to each file.
        #       3. for each file, do a search content on the json file.
        #       4. retrieve content for each file.
        #       5. process content: sorted, unique
        #       6. output process: an object that can be __str__-ed.

        results = cmd.execute().items

        self.assertEqual(results, [
            {
                'create.json': [
                    'to be the first to portray (a particular role in a play)'
                ]
            },
            {
                "do.json": [
                    "to produce or appear in (a play, etc.)",
                    "to play the role of"
                ]
            },
            {"perform.json": [
                "to carry out or execute an action or process; esp., to take part in a musical program, "
                "act in a play, dance, etc. before an audience"
            ]}
        ])

    def test_searchResultText_fromJsonObject(self):
        cmd = DefsCommand("play")
        cmd.set_dir_path(self.dir_path)

        with patch.object(JsonSearch, "__call__") as mock_search:
            mock_search.return_value = [
                {'create.json': ['to be the first to portray (a particular role in a play)']},
                {"do.json": ["to produce or appear in (a play, etc.)", "to play the role of"]},
            ]

            str_result = str(cmd.execute())

            str_result = str_result.replace(BOLDBLACK, "")
            str_result = str_result.replace(BOLDRED, "")
            str_result = str_result.replace(RESET, "")

            self.assertEqual(
                "[create.json]\n"
                "o) to be the first to portray (a particular role in a play)\n\n"
                "[do.json]\n"
                "o) to produce or appear in (a play, etc.)\n"
                "o) to play the role of\n\n\n"
                , str_result
            )


if __name__ == '__main__':
    unittest.main()
