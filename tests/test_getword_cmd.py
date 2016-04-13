import unittest
import json
from unittest.mock import patch
import os

from src import commands
from src.cmd_getword import GetWordCommand, WordInvalidError
from src.word import RedirectError


class TestGetWordCommand(unittest.TestCase):
    word_exp_content = None

    @classmethod
    def setUpClass(cls):
        TestGetWordCommand.word_exp_content = None

        os.chdir("./do")
        exp_do = "expected_do.json"

        with open(exp_do, "r") as f:
            TestGetWordCommand.word_exp_content = json.load(f)

    def setUp(self):
        self.word = "do"

    def test_command_getword_returns_GetWord_class(self):
        input_str = self.word

        command = commands.match_command(input_str)
        self.assertIsInstance(command, GetWordCommand)

    def test_command_do_saves_json_file(self):
        cmd = GetWordCommand()

        # when calling execute, I expect the json file to be downloaded.
        # I assume the content is correct
        # it needs to know where to put the file, but I could receive it as string.
        with patch.object(GetWordCommand, '_fetch_content') as mock:
            mock.return_value = TestGetWordCommand.word_exp_content

            json_content = cmd.execute(self.word)

        self.assertEqual(TestGetWordCommand.word_exp_content, json_content)

    def test_ill_formed_word_raises_exception(self):
        with patch.object(GetWordCommand, '_fetch_content'):
            cmd = GetWordCommand()

            with self.assertRaises(WordInvalidError):
                cmd.execute("a;&%&i")

    def test_space_transforms_to_dash_for_word(self):
        with patch.object(GetWordCommand, '_fetch_content') as mock_fetch:
            cmd = GetWordCommand()

            cmd.execute("do by")

            mock_fetch.assert_called_once_with("do-by")


if __name__ == '__main__':
    unittest.main()
