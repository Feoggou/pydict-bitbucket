from src.word_handler import *
from src import cmd_getword
from src.cmd_getword import GetWordCommand

import unittest
import sys
import io
import os
import json

from unittest.mock import patch
from unittest.mock import call
from unittest import mock


mock_out = mock.Mock()


# TODO: Find a better name!
class TestWordHandler(unittest.TestCase):
    word_exp_print = None
    word_exp_json = None

    @classmethod
    def setUpClass(cls):
        TestWordHandler.expected_json = None
        TestWordHandler.expected_print = None

        os.chdir("./do")
        exp_json = "expected_do.json"
        exp_print = "expected_do.txt"

        with open(exp_json, "r") as f:
            TestWordHandler.word_exp_json = json.load(f)

        with open(exp_print, "r") as f:
            TestWordHandler.word_exp_print = f.read()

    def setUp(self):
        self.DIR_PATH = "./test-data"
        mock_out.reset_mock()

    def tearDown(self):
        pass

    # -------------------- TESTS --------------------
    @patch("src.word_handler.output_msg", mock_out)
    def test_word_do_is_requested_it_is_retrieved(self):
        word_handler = WordHandler(self.DIR_PATH)

        with patch.object(WordHandler, '_already_exists') as mock_exists:
            mock_exists.return_value = False

            with patch.object(WordHandler, '_save_json') as mock_exists:
                mock_exists.return_value = False

                with patch.object(GetWordCommand, '_fetch_content') as mock:
                    mock.return_value = TestWordHandler.word_exp_print
                    word_handler.get("do")

        mock_out.assert_called_once_with(TestWordHandler.word_exp_print)

    @patch("src.word_handler.output_msg", mock_out)
    def test_word_do_is_requested_so_json_is_saved(self):
        word_handler = WordHandler(self.DIR_PATH)

        with patch.object(WordHandler, '_already_exists') as mock_exists:
            mock_exists.return_value = False

            with patch.object(WordHandler, '_save_json') as mock_save:
                with patch.object(GetWordCommand, '_fetch_content') as mock_fetch:
                    mock_fetch.return_value = TestWordHandler.word_exp_print
                    word_handler.get("do")

                mock_save.assert_called_once_with("do", TestWordHandler.word_exp_print)

    @patch("src.word_handler.output_msg", mock_out)
    def test_word_ill_formed_fails_and_error_is_printed(self):
        word_handler = WordHandler(self.DIR_PATH)

        # the exception must be risen, caught, message printed.
        word_handler.get("a;&%&i")

        mock_out.assert_called_once_with("Invalid word: a;&%&i")

    @patch("src.word_handler.output_msg", mock_out)
    def test_worddoesnotexist_is_not_found_so_error_is_printed(self):
        word_handler = WordHandler(self.DIR_PATH)

        # the exception must be risen, caught, message printed.
        with patch.object(GetWordCommand, '_fetch_content') as mock:
            mock.side_effect = RedirectError("american?q=worddoesnotexist")
            word_handler.get("worddoesnotexist")

        mock_out.assert_called_once_with("The word 'worddoesnotexist' was not found!")

    @patch("src.word_handler.output_msg", mock_out)
    def test_word_commoditization_is_not_found_and_have_no_redirect_available_so_print_error(self):
        word_handler = WordHandler(self.DIR_PATH)

        # the exception must be risen, caught, message printed.
        with patch.object(GetWordCommand, '_fetch_content') as mock:
            mock.side_effect = RedirectError("american?q=commoditization")
            word_handler.get("commoditization")

        mock_out.assert_called_once_with("The word 'commoditization' was not found!")

    @patch("src.word_handler.output_msg", mock_out)
    def test_word_fazed_is_not_found_ask_user_for_redirection_he_answers_yes_so_retrieve_faze(self):
        with patch('src.cmd_getword.GetWordCommand', autospec=GetWordCommand) as MockGetWordCommand:
            mock_obj = MockGetWordCommand.return_value
            mock_obj.execute.side_effect = [RedirectError("faze"), "faze_content_json"]

            word_handler = WordHandler(self.DIR_PATH)

            with patch.object(WordHandler, '_save_json') as mock_save:
                with patch('builtins.input') as mock_input:
                    mock_input.return_value = "Yes"

                    # word is not found on disk, so it tries downloading it, it finds redirect,
                    # so it asks the user "Word 'fazed' not found. Would you like to get word 'faze' instead?"
                    # He answers "yes", so the GetWordCommand is called once again, with word "faze", which
                    # returns what we need.
                    word_handler.get("fazed")

                    mock_input.assert_called_once_with(
                        "Word 'fazed' not found. Would you like to get word 'faze' instead?")

            calls = [call("fazed"), call("faze")]
            mock_obj.set_argument_value.assert_has_calls(calls)

        mock_out.assert_called_once_with("faze_content_json")

    @patch("src.word_handler.output_msg", mock_out)
    def test_word_creat_not_found_ask_user_for_redirecttion_he_answers_yes_so_retrieve_create(self):
        with patch('src.cmd_getword.GetWordCommand', autospec=GetWordCommand) as MockGetWordCommand:
            mock_obj = MockGetWordCommand.return_value
            mock_obj.execute.side_effect = [RedirectError("create"), "create_content_json"]

            word_handler = WordHandler(self.DIR_PATH)
            with patch.object(WordHandler, '_save_json') as mock_save:
                with patch('builtins.input') as mock_input:
                    mock_input.return_value = "Yes"

                    word_handler.get("creat")

                    mock_input.assert_called_once_with(
                        "Word 'creat' not found. Would you like to get word 'create' instead?")

            calls = [call("creat"), call("create")]
            mock_obj.set_argument_value.assert_has_calls(calls)

        # TODO: What EXACTLY do I want to test here: that the question was asked correctly? that the calls were correct? that the content was retrieved?
        mock_out.assert_called_once_with("create_content_json")

    def test_word_unintended_is_not_found_and_user_does_not_accept_the_redirect_version_un(self):
        with patch('src.cmd_getword.GetWordCommand', autospec=GetWordCommand) as MockGetWordCommand:
            mock_obj = MockGetWordCommand.return_value
            mock_obj.execute.side_effect = RedirectError("un-")

            word_handler = WordHandler(self.DIR_PATH)
            with patch('builtins.input') as mock_input:
                mock_input.return_value = "No"

                word_handler.get("unintended")

                mock_input.assert_called_once_with("Word 'unintended' not found. Would you like to get word 'un-' instead?")

    def test_word_do_already_exists_so_it_calls_print_word(self):
        word_handler = WordHandler(self.DIR_PATH)

        with patch.object(WordHandler, '_already_exists') as mock_exists:
            mock_exists.return_value = True
            with patch.object(WordHandler, '_print_word') as mock_print:
                mock_print.side_effect = mock_out(TestWordHandler.word_exp_print)
                word_handler.get("do")

        mock_out.assert_called_once_with(TestWordHandler.word_exp_print)

    def test_save_json_saves_content(self):
        word_handler = WordHandler(self.DIR_PATH)

        word = "do"
        content = "json_content"

        m = mock.mock_open()
        with patch("builtins.open", m):
            mock_file_obj = m.return_value

            word_handler._save_json(word, content)

            file_path = os.path.join(self.DIR_PATH, word)
            m.assert_called_once_with(file_path, "w")
            mock_file_obj.write.assert_called_once_with(content)


if __name__ == "__main__":
    unittest.main()

# TODO: find a better name for it!
