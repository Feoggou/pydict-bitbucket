import unittest
import json
from unittest.mock import patch
import os

from src import commands
from src.cmd_default import GetWordCommand, WordInvalidError
from src.word import RedirectError


class TestDefaultCommand(unittest.TestCase):
    word_exp_content = None

    @classmethod
    def setUpClass(cls):
        TestDefaultCommand.word_exp_content = None

        os.chdir("./do")
        exp_do = "expected_do.json"

        with open(exp_do, "r") as f:
            TestDefaultCommand.word_exp_content = json.load(f)

    def setUp(self):
        self.word = "do"

    def test_command_default_returns_Default_class(self):
        input_str = self.word

        command = commands.match_command(input_str)
        self.assertIsInstance(command, GetWordCommand)
        self.assertEqual(self.word, command.get_argument_value())

    def test_command_do_saves_json_file(self):
        cmd = GetWordCommand()
        cmd.set_argument_value(self.word)

        # when calling execute, I expect the json file to be downloaded.
        # I assume the content is correct
        # it needs to know where to put the file, but I could receive it as string.
        with patch.object(GetWordCommand, '_fetch_content') as mock:
            mock.return_value = TestDefaultCommand.word_exp_content
            with patch.object(GetWordCommand, '_word_already_exists') as mock_exists:
                mock_exists.return_value = False

                json_content = cmd.execute()

        self.assertEqual(TestDefaultCommand.word_exp_content, json_content)

    def test_ill_formed_word_raises_exception(self):
        with patch.object(GetWordCommand, '_fetch_content'):
            cmd = GetWordCommand()
            cmd.set_argument_value("a;&%&i")

            with self.assertRaises(WordInvalidError):
                cmd.execute()

    def test_space_transforms_to_dash_for_word(self):
        with patch.object(GetWordCommand, '_fetch_content'):
            cmd = GetWordCommand()
            cmd.set_argument_value("do by")

            with patch.object(GetWordCommand, '_word_already_exists') as mock_exists:
                mock_exists.return_value = False

                cmd.execute()

            word = cmd.get_argument_value()
            self.assertEqual("do-by", word)

    def test_call_print_if_word_exists(self):
        with patch.object(GetWordCommand, '_fetch_content'):
            with patch.object(GetWordCommand, '_word_already_exists') as mock_exists:
                mock_exists.return_value = True

                with patch.object(GetWordCommand, '_call_printer') as mock_printer:
                    cmd = GetWordCommand()
                    cmd.set_argument_value("do")

                    cmd.execute()

                    mock_printer.assert_called_with()

    def test_on_redirect_if_auto_then_do_redirect(self):
        with patch.object(GetWordCommand, '_fetch_content') as mock_fetch_content:
            mock_fetch_content.side_effect = RedirectError("/url-dummy")

            with patch.object(GetWordCommand, '_word_already_exists') as mock_exists:
                mock_exists.return_value = False

                with patch.object(GetWordCommand, '_redirect_to') as mock_redirect:
                    mock_redirect.return_value = TestDefaultCommand.word_exp_content

                    cmd = GetWordCommand(auto=True)
                    cmd.set_argument_value("do")

                    content = cmd.execute()

                    self.assertEqual(TestDefaultCommand.word_exp_content, content)

    def test_on_redirect_if_not_auto_then_ask_user_answers_no(self):
        with patch.object(GetWordCommand, '_fetch_content') as mock_fetch_content:
            mock_fetch_content.side_effect = RedirectError("/url-dummy")

            with patch.object(GetWordCommand, '_word_already_exists') as mock_exists:
                mock_exists.return_value = False

                with patch('builtins.input') as mock_input:
                    mock_input.return_value = "No"

                    cmd = GetWordCommand(auto=False)
                    cmd.set_argument_value("do")

                    content = cmd.execute()

                    self.assertEqual(None, content)

    def test_on_redirect_if_not_auto_then_ask_user_answers_yes(self):
        with patch.object(GetWordCommand, '_fetch_content') as mock_fetch_content:
            mock_fetch_content.side_effect = RedirectError("/url-dummy")

            with patch.object(GetWordCommand, '_word_already_exists') as mock_exists:
                mock_exists.return_value = False

                with patch('builtins.input') as mock_input:
                    mock_input.return_value = "Yes"

                    with patch.object(GetWordCommand, '_redirect_to') as mock_redirect:
                        mock_redirect.return_value = TestDefaultCommand.word_exp_content

                        cmd = GetWordCommand(auto=False)
                        cmd.set_argument_value("do")

                        content = cmd.execute()

                        self.assertEqual(TestDefaultCommand.word_exp_content, content)


if __name__ == '__main__':
    unittest.main()
