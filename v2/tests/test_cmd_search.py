import unittest
from unittest import mock
from unittest.mock import patch

from src.cmd_search import Search
from src.json_print import JsonPrinter

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
    """def test_dummy(self):
        # INPUT: search(do)
        # CONTAINER HAS:      "do.def", "do.learn", "do.syn", "to-do-something.def", "doing.def", "smth-do.learn"
        # EXPECTED RESULT:    find files "do.def; do.learn; do.syn", "to-do-something.def"
        result = process_input("search(do)")
        self.assertEqual(["do.def", "do.learn", "do.syn", "to-do-something.def"], result)"""

    def test_input_do(self):
        with patch.object(Search, "search") as mock_search:
            mock_search.return_value = "dummy_result"
            with patch.object(JsonPrinter, "print_results") as mock_print:
                process_input("search(do)")

        mock_search.assert_called_once_with("do")
        mock_print.assert_called_once_with(mock.ANY)


if __name__ == '__main__':
    unittest.main()
