from src.word_handler import *
from src.cmd_getword import GetWordCommand

import unittest

from unittest.mock import patch
from unittest.mock import call
from unittest import mock


mock_out = mock.Mock()


# TODO: Find a better name!
class TestWordHandler(unittest.TestCase):
    def setUp(self):
        self.DIR_PATH = "./test-data"
        mock_out.reset_mock()

    # -------------------- TESTS --------------------
    @patch("src.word_handler.output_msg", mock_out)
    def test_when_do_isRequested_contentIsSavedAndPrinted(self):
        word_handler = WordHandler(self.DIR_PATH)

        with patch.object(WordHandler, '_already_exists') as mock_exists:
            mock_exists.return_value = False
            with patch.object(WordHandler, '_save_json') as mock_save:
                with patch.object(GetWordCommand, '_fetch_content') as mock_fetch:
                    mock_fetch.return_value = "json_content"

                    word_handler.get("do")

                mock_save.assert_called_once_with("do", "json_content")
        mock_out.assert_called_once_with("json_content")

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

            calls = [call("creat"), call("create")]
            mock_obj.set_argument_value.assert_has_calls(calls)
        mock_out.assert_called_once_with("create_content_json")

    @patch("src.word_handler.output_msg", mock_out)
    def test_onRedirectionError_outputMessageIsCorrect(self):
        word_orig = "somethin"
        word_redir = "something"

        with patch.object(GetWordCommand, 'execute') as mock_exec:
            mock_exec.side_effect = RedirectError(word_redir)
            with patch.object(WordHandler, '_already_exists') as mock_exists:
                mock_exists.return_value = False
                with patch('builtins.input') as mock_input:
                    mock_input.return_value = "No"

                    word_handler = WordHandler(self.DIR_PATH)
                    word_handler.get(word_orig)

                    mock_input.assert_called_once_with(
                        "Word '{}' not found. Would you like to get word '{}' instead?".format(word_orig, word_redir))

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
                mock_print.side_effect = mock_out("printed_content")
                with patch.object(GetWordCommand, 'execute') as mock_exec:
                    word_handler.get("do")

                    mock_exec.assert_not_called()
        mock_out.assert_called_once_with("printed_content")


if __name__ == "__main__":
    unittest.main()

# TODO: find a better name for it!
