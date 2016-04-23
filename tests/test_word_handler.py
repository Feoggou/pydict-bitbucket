import unittest

from unittest.mock import patch
from unittest.mock import call
from unittest import mock
import copy

from src.word_handler import *
from src.cmd_getword import GetWordCommand

mock_out = mock.Mock()


class DeepCopyMock(mock.MagicMock):
    def _mock_call(self, *args, **kwargs):
        return super(DeepCopyMock, self)._mock_call(*copy.deepcopy(args), **copy.deepcopy(kwargs))


# TODO: Find a better name!
class TestWordHandler(unittest.TestCase):
    def setUp(self):
        self.DIR_PATH = "./test-data"

        with open("doing.json") as f:
            self.doing_stripped_content = json.load(f)

        with open("doing_with_do.json") as f:
            self.doing_full_content = json.load(f)

        with open("do/expected_do.json") as f:
            self.do_content = json.load(f)

        mock_out.reset_mock()

    @patch.object(WordHandler, '_print_json_content', mock_out)
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

    @patch.object(WordHandler, '_print_json_content', mock_out)
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
            mock_obj.execute.assert_has_calls(calls)
        mock_out.assert_called_once_with("faze_content_json")

    @patch.object(WordHandler, '_print_json_content', mock_out)
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
            mock_obj.execute.assert_has_calls(calls)
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

    @patch.object(WordHandler, '_print_word', mock_out)
    @patch.object(WordHandler, '_print_json_content', mock_out)
    def test_whenWordIsRetrievedTwice_2ndTimeDoesntDownload(self):
        word_handler = WordHandler(self.DIR_PATH)
        os.makedirs(self.DIR_PATH, exist_ok=True)

        for x in os.listdir(self.DIR_PATH):
            os.remove(os.path.join(self.DIR_PATH, x))

        with patch.object(GetWordCommand, '_fetch_content') as mock_fetch:
            mock_fetch.return_value = "json_content"

            word_handler.get("do")
            word_handler.get("do")

            mock_fetch.assert_called_once_with("do")

    @patch.object(WordHandler, "_save_json")
    @patch.object(WordHandler, "_print_json_content")
    @patch("unittest.mock.MagicMock", new=DeepCopyMock)
    def test_when_doing_isRequested_removeSubword(self, mock_save, mock_print):
        word_handler = WordHandler(self.DIR_PATH)

        with patch.object(WordHandler, "_already_exists") as mock_exists:
            mock_exists.return_value = False
            with patch.object(GetWordCommand, '_fetch_content') as mock_content:
                mock_content.return_value = self.doing_full_content
                with patch.object(WordHandler, "get_subword") as mock_get_subword:
                    mock_get_subword.side_effect = [False]

                    result = word_handler.get("doing")

        mock_get_subword.assert_called_once_with("do")
        self.assertEqual(self.doing_stripped_content, result)
        mock_save.assert_called_once_with("doing", self.doing_stripped_content)
        mock_print.assert_called_once_with("doing", self.doing_stripped_content)

    @patch.object(WordHandler, "_save_json")
    @patch.object(WordHandler, "_print_json_content")
    @patch("unittest.mock.MagicMock", new=DeepCopyMock)
    def test_when_do_isRequested_ask_removeSubword_No(self, mock_save, mock_print):
        word_handler = WordHandler(self.DIR_PATH)

        with patch.object(WordHandler, "_already_exists") as mock_exists:
            mock_exists.return_value = False
            with patch.object(WordHandler, '_get_word_definition') as mock_content:
                mock_content.return_value = self.do_content
                with patch.object(WordHandler, "get_subword") as mock_get_subword:
                    mock_get_subword.side_effect = [True, True, True]

                    result = word_handler.get("do")

        mock_get_subword.assert_has_calls([call('Do or do'), call('DO or D.O.')])
        self.assertEqual(self.do_content, result)

if __name__ == "__main__":
    unittest.main()

# TODO: find a better name for it!
