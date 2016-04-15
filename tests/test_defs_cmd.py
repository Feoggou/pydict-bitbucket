import unittest
import json
from unittest.mock import patch
import os

from src import commands
from src.cmd_defs import DefsCommand


class TestDefsCommand(unittest.TestCase):
    # word_exp_content = None

    @classmethod
    def setUpClass(cls):
        TestDefsCommand.word_exp_content = None

        # os.chdir("./do")
        # exp_do = "expected_do.json"

        # with open(exp_do, "r") as f:
        #     TestDefsCommand.word_exp_content = json.load(f)

    def setUp(self):
        # self.word = "do"
        self.dir_path = "./test-data"

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

        with patch.object(DefsCommand, "_search_files") as mock_files:
            mock_files.return_value = ["a.json", "do.json", "b.json", "perform.json", "c.json"]

            with patch.object(DefsCommand, "_search_content") as mock_content:
                do_list = ["to produce or appear in (a play, etc.)", "to play the role of"]
                perform_list = ["to carry out or execute an action or process; esp., to take part in a musical "
                                "program, act in a play, dance, etc. before an audience"]

                mock_content.side_effect = [{}, {"do.json": do_list}, {}, {"perform.json": perform_list}, {}]

                with patch.object(DefsCommand, "_process_contents") as mock_processed:
                    mock_processed.return_value = [{"do.json": do_list}, {"perform.json": perform_list}]

                    results = cmd.execute()  # .value

        self.assertEqual(results, [
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

    def test_searchContent_opensFileAndCallsToSearchContent(self):
        cmd = DefsCommand("")
        cmd.set_dir_path(self.dir_path)

        # must: open file "do.json"
        # json.load info from it.
        # call json_search("play)
        # return: the list of defs.
        with patch.object(DefsCommand, "_search_json") as mock_search:
            mock_search.return_value = ["to produce or appear in (a play, etc.)", "to play the role of"]
            results = cmd._search_content("do.json", "play")

        self.assertEqual(results, ["to produce or appear in (a play, etc.)", "to play the role of"])


if __name__ == '__main__':
    unittest.main()
