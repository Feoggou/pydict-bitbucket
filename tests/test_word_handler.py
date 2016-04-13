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
        # TODO: expected_json, expected_print -- we can use dummy values.
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
    def test_when_do_isRequested_contentIsSavedAndPrinted(self):
        word_handler = WordHandler(self.DIR_PATH)

        with patch.object(WordHandler, '_already_exists') as mock_exists:
            mock_exists.return_value = False

            with patch.object(WordHandler, '_save_json') as mock_save:
                with patch.object(GetWordCommand, '_fetch_content') as mock:
                    mock.return_value = TestWordHandler.word_exp_json

                    word_handler.get("do")

                mock_save.assert_called_once_with("do", TestWordHandler.word_exp_json)
        mock_out.assert_called_once_with(TestWordHandler.word_exp_json)

    @patch("src.word_handler.output_msg", mock_out)
    def test_whenWordIsIllFormed_failAndOutputError(self):
        word_handler = WordHandler(self.DIR_PATH)

        with patch.object(WordHandler, '_already_exists') as mock_exists:
            mock_exists.return_value = False

            # the exception must be risen, caught, message printed.
            word_handler.get("a;&%&i")

        mock_out.assert_called_once_with("Invalid word: a;&%&i")

    @patch("src.word_handler.output_msg", mock_out)
    def test_whenWord_worddoesnotexist_isNotFound_and_foundNoRelated_outputError(self):
        word_handler = WordHandler(self.DIR_PATH)

        with patch.object(WordHandler, '_already_exists') as mock_exists:
            mock_exists.return_value = False

            with patch.object(GetWordCommand, '_fetch_content') as mock_fetch:
                mock_fetch.side_effect = RedirectError("american?q=worddoesnotexist")

                # the exception must be risen, caught, message printed.
                word_handler.get("worddoesnotexist")

        mock_out.assert_called_once_with("The word 'worddoesnotexist' was not found!")

    @patch("src.word_handler.output_msg", mock_out)
    def test_when_commoditization_isNotFound_and_foundNoRelated_outputError(self):
        word_handler = WordHandler(self.DIR_PATH)

        with patch.object(WordHandler, '_already_exists') as mock_exists:
            mock_exists.return_value = False
            with patch.object(GetWordCommand, '_fetch_content') as mock:
                mock.side_effect = RedirectError("american?q=commoditization")

                # the exception must be risen, caught, message printed.
                word_handler.get("commoditization")

        mock_out.assert_called_once_with("The word 'commoditization' was not found!")

    @patch("src.word_handler.output_msg", mock_out)
    def test_when_fazed_isNotFound_askUserForRedirection_Yes_retrieve_faze(self):
        with patch('src.cmd_getword.GetWordCommand', autospec=GetWordCommand) as MockGetWordCommand:
            mock_obj = MockGetWordCommand.return_value
            mock_obj.execute.side_effect = [RedirectError("faze"), "faze_content_json"]

            with patch.object(WordHandler, '_already_exists') as mock_exists:
                mock_exists.return_value = False

                with patch.object(WordHandler, '_save_json'):
                    with patch('builtins.input') as mock_input:
                        mock_input.return_value = "Yes"

                        word_handler = WordHandler(self.DIR_PATH)

                        # 1. word "fazed" is not found on disk, so it tries downloading it.
                        # 2. Redirection is returned.
                        # 3. Asks the user if he wants "faze"
                        # 4. User chooses "yes"
                        # 5. GetWordCommand is called once again, with word "faze", which yields content
                        word_handler.get("fazed")

                        # TODO: should test this in a separate test function!
                        mock_input.assert_called_once_with(
                            "Word 'fazed' not found. Would you like to get word 'faze' instead?")

            calls = [call("fazed"), call("faze")]
            mock_obj.set_argument_value.assert_has_calls(calls)
        mock_out.assert_called_once_with("faze_content_json")

    @patch("src.word_handler.output_msg", mock_out)
    def test_when_creat_isNotFound_askUserForRedirection_Yes_retrieve_create(self):
        with patch('src.cmd_getword.GetWordCommand', autospec=GetWordCommand) as MockGetWordCommand:
            mock_obj = MockGetWordCommand.return_value
            mock_obj.execute.side_effect = [RedirectError("create"), "create_content_json"]

            with patch.object(WordHandler, '_already_exists') as mock_exists:
                mock_exists.return_value = False

                with patch.object(WordHandler, '_save_json'):
                    with patch('builtins.input') as mock_input:
                        mock_input.return_value = "Yes"

                        word_handler = WordHandler(self.DIR_PATH)
                        word_handler.get("creat")

                        mock_input.assert_called_once_with(
                            "Word 'creat' not found. Would you like to get word 'create' instead?")

            calls = [call("creat"), call("create")]
            mock_obj.set_argument_value.assert_has_calls(calls)
        # TODO: What EXACTLY do I want to test here: that the question was asked correctly? that the calls were correct? that the content was retrieved?
        mock_out.assert_called_once_with("create_content_json")

    def test_when_unintended_isNotFoundAnd_askUserForRedirection_No_cancel(self):
        with patch('src.cmd_getword.GetWordCommand', autospec=GetWordCommand) as MockGetWordCommand:
            mock_obj = MockGetWordCommand.return_value
            mock_obj.execute.side_effect = RedirectError("un-")

            with patch.object(WordHandler, '_already_exists') as mock_exists:
                mock_exists.return_value = False

                with patch.object(WordHandler, '_save_json') as mock_save:
                    with patch('builtins.input') as mock_input:
                        mock_input.return_value = "No"

                        word_handler = WordHandler(self.DIR_PATH)
                        word_handler.get("unintended")

                        mock_input.assert_called_once_with("Word 'unintended' not found. Would you like to get word 'un-' instead?")
                    mock_save.assert_not_called()

    def test_do_alreadyExists_dontDownload_callPrintWord(self):
        word_handler = WordHandler(self.DIR_PATH)

        with patch.object(WordHandler, '_already_exists') as mock_exists:
            mock_exists.return_value = True
            with patch.object(WordHandler, '_print_word') as mock_print:
                mock_print.side_effect = mock_out(TestWordHandler.word_exp_print)

                with patch.object(GetWordCommand, 'execute') as mock_exec:
                    word_handler.get("do")

                    mock_exec.assert_not_called()
        mock_out.assert_called_once_with(TestWordHandler.word_exp_print)


if __name__ == "__main__":
    unittest.main()

# TODO: find a better name for it!
