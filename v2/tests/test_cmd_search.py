import unittest
from unittest import mock
from unittest.mock import patch

from src.cmd_search import Search
from src.json_collector import JsonCollector
from src.json_load import JsonLoader

from src.input_processor import process_input, print_syn


# SEARCH: search exact (i.e. "contains" as word)
# RSEARCH: search as regular expression
# search in: words, derived forms, etc.
#           options: vb, vt, vi, noun, etc.
#           does not search into examples. for that, we will have an "examples()"
#           also, we will have a "mine()", "myex()", "mydefs()", etc.
#           when searching in synonyms, perhaps we should pick a def or smth - in learn?
#           searches regardless of "known" and "useful".
# TODO: wsearch will search word-based (i.e. pick all word forms, then start search with each)
#       TAG will search solely based on tag
class TestSearch(unittest.TestCase):
    def test_input_do_calls_search_and_print(self):
        with patch.object(Search, "search") as mock_search:
            mock_search.return_value = "dummy_result"
            with patch("src.input_processor.output_text") as mock_print:
                process_input("search(do)")

        mock_search.assert_called_once_with("do")
        mock_print.assert_called_once_with(mock.ANY)

    @patch.object(Search, "find_word_forms")
    def test_search_do_callsFindFiles(self, mock_find_word_forms):
        op = Search()

        with patch.object(Search, 'find_files') as mock_find_files:
            op.search("do")

        mock_find_files.assert_called_once_with("do")

    def test_findFiles_retrievesFileNames(self):
        op = Search()

        with patch.object(Search, "collect_filenames") as mock_collect:
            mock_collect.return_value = [
                "do.def", "do.learn", "do.syn", "to-do-something.def", "doing.def", "smth-do.learn", "_do.def"
            ]

            result = op.find_files("do")

        self.assertEqual(["do.def", "do.learn", "do.syn", "to-do-something.def", "smth-do.learn"], result)

    @patch.object(Search, "find_word_forms")
    def test_search_retrievesFileNames(self, mock_word_forms):
        op = Search()

        with patch.object(Search, "collect_filenames") as mock_collect:
            mock_collect.return_value = [
                "do.def", "do.learn", "do.syn", "to-do-something.def", "doing.def", "smth-do.learn", "_do.def"
            ]

            result = op.search("do")

        self.assertEqual(["do.def", "do.learn", "do.syn", "to-do-something.def", "smth-do.learn"], result.file_names)

    def test_search_callsFindWordForms(self):
        op = Search()

        with patch.object(Search, "find_word_forms") as mock_find:
            op.search("do")

        mock_find.assert_called_once_with("do")

    def test_findWordForms_collectsWordsAndMatches(self):
        op = Search()

        with patch.object(JsonLoader, "load") as mock_load:
            mock_load.return_value = "dummy_content"
            with patch.object(Search, "collect_filenames") as mock_filenames:
                mock_filenames.return_value = ["abcd.def"]
                with patch.object(JsonCollector, "collect_word_forms") as mock_collect:
                    mock_collect.return_value = ["do", "a", "doing", "do or done", "whatever", "doing and do"]

                    result = op.find_word_forms("do")

        self.assertEqual({"abcd.def": ["do", "do or done", "doing and do"]}, result)


if __name__ == '__main__':
    unittest.main()
