import unittest
from unittest import mock
from unittest.mock import patch, call
import os
import json

from src.input_processor import process_input
from src.json_save import JsonSaver
from src.json_print import JsonPrinter
from src.content_retrieval import ContentRetrieval

from src import config


class GetWordCmdTest(unittest.TestCase):
    do_def_json = None
    do_learn_json = None
    do_syn_json = None

    @classmethod
    def retrieve_json_content(cls, file_path: str):
        with open(file_path) as f:
            return json.load(f)

    @classmethod
    def setUpClass(cls):
        path = os.path.dirname(os.path.abspath(__file__))

        cls.do_def_json = cls.retrieve_json_content(os.path.join(path, "json_files", "expected_do.def"))
        cls.do_learn_json = cls.retrieve_json_content(os.path.join(path, "json_files", "expected_do.learn"))
        cls.do_syn_json = cls.retrieve_json_content(os.path.join(path, "json_files", "expected_do.syn"))

    def test_get_word_do_defs(self):
        """
        input: string "do"
        expected result: call a "print" function and save a "do.def" and "do.syn" file (with correct params)
                         for the moment it doesn't matter the content of the save, nor what is printed.
        """

        defs_content = "defs_content_dummy"
        learn_content = "learn_content_dummy"
        syn_content = "syn_content_dummy"

        with patch.object(ContentRetrieval, 'get_def_content') as mock_get_defs:
            mock_get_defs.return_value = defs_content, learn_content
            with patch.object(ContentRetrieval, 'get_syn_content') as mock_get_syns:
                mock_get_syns.return_value = syn_content
                with patch.object(JsonSaver, 'save') as mock_save_defs:
                    with patch.object(JsonPrinter, 'print') as mock_print:
                        with patch.object(JsonPrinter, 'print_learn') as mock_print_learn:
                            process_input("do")

        calls = [call("do.def", defs_content), call("do.learn", learn_content), call("do.syn", syn_content)]
        mock_save_defs.assert_has_calls(calls)
        mock_print.assert_called_once_with(defs_content)
        mock_print_learn.assert_called_once_with(learn_content)

    def test_get_word_tall_defs(self):
        """
        input: string "tall"
        expected result: call a "print" function and save a "tall.def" and "tall.syn" file.
                         for the moment it doesn't matter the content of the save, nor what is printed.
        """

        defs_content = "defs_content_dummy"
        learn_content = "learn_content_dummy"
        syn_content = "syn_content_dummy"

        with patch.object(ContentRetrieval, 'get_def_content') as mock_get_defs:
            mock_get_defs.return_value = defs_content, learn_content
            with patch.object(ContentRetrieval, 'get_syn_content') as mock_get_syns:
                mock_get_syns.return_value = syn_content
                with patch.object(JsonSaver, 'save') as mock_save_defs:
                    with patch.object(JsonPrinter, 'print') as mock_print:
                        with patch.object(JsonPrinter, 'print_learn') as mock_print_learn:
                            process_input("tall")

        calls = [call("tall.def", defs_content), call("tall.learn", learn_content), call("tall.syn", syn_content)]
        mock_save_defs.assert_has_calls(calls)
        mock_print.assert_called_once_with(defs_content)
        mock_print_learn.assert_called_once_with(learn_content)

    def test_get_word_do_defs_usingRealFetcher(self):
        """uses  "Real" HtmlFetcher"""

        with patch.object(JsonSaver, 'save') as mock_save_defs:
            with patch.object(JsonPrinter, 'print'):
                with patch.object(JsonPrinter, 'print_learn'):
                    process_input("do")

        calls = [call("do.def", self.do_def_json), call("do.learn", self.do_learn_json), call("do.syn", self.do_syn_json)]
        mock_save_defs.assert_has_calls(calls)


if __name__ == '__main__':
    unittest.main()
