import unittest
import json
from unittest.mock import patch
import os

from src import commands
from src.cmd_defs import DefsCommand
from src.colors import *
from src.json_seeker import *


class TestDefsCommand(unittest.TestCase):
    do_exp_content = None
    word_exp_content = None

    @classmethod
    def setUpClass(cls):
        TestDefsCommand.do_exp_content = None

        exp_do = "./do/expected_do.json"
        exp_word = "word_json_read.json"

        with open(exp_do, "r") as f:
            TestDefsCommand.do_exp_content = json.load(f)

        with open(exp_word, "r") as f:
            TestDefsCommand.word_exp_content = json.load(f)

    def setUp(self):
        # self.word = "do"
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

    def test_searchContent_opensFileAndCallsToSearchContent(self):
        seeker = JsonSearch(self.dir_path, "play")

        # must: open file "do.json"
        # json.load info from it.
        # call json_search("play)
        # return: the list of defs.
        results = seeker._search_content("do.json", "play")

        self.assertEqual(results, {"do.json": ["to produce or appear in (a play, etc.)", "to play the role of"]})

    def test_searchJsonFindsItems(self):
        seeker = JsonSearch(self.dir_path, "play")

        # A. must search in:
        # 1. def_groups[i] / semantics
        # 2. def_groups[i] / gram_groups[j] // defs[k]
        # 3. translations[i]
        # B. must sort & unique them
        # C. must find the items in A that contain word "play"

        result = seeker._search_json(TestDefsCommand.do_exp_content, "play")

        self.assertEqual(result, ["to produce or appear in (a play, etc.)", "to play the role of"])

    def test_getSemantics_retrievesAll(self):
        seeker = JsonSearch(self.dir_path, "play")

        semantics = seeker._get_semantics(TestDefsCommand.word_exp_content)

        self.assertEqual(semantics, ["<semantics_content_here>"])

    def test_getDefs_retrievesAll(self):
        seeker = JsonSearch(self.dir_path, "play")

        defs = seeker._get_defs(TestDefsCommand.word_exp_content)

        self.assertEqual(len(defs), 30)

    def test_getTranslations_retrievesAll(self):
        seeker = JsonSearch(self.dir_path, "play")

        transls = seeker._get_translations(TestDefsCommand.word_exp_content)

        self.assertEqual(transls, ["[transl.] When you do something, you take some action or perform an activity or task.I was trying to do some work. done"])

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
