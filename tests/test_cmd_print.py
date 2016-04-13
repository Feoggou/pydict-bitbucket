import unittest
import os
import json
import shutil

from unittest import mock
from unittest.mock import patch

from src.cmd_print import PrintCommand


class TestCommandPrint(unittest.TestCase):
    word_exp_print = None
    word_exp_json = None
    dir_path = "./test-data"

    @classmethod
    def setUpClass(cls):
        TestCommandPrint.expected_json = None
        TestCommandPrint.expected_print = None

        os.chdir("./do")
        exp_json = "expected_do.json"
        exp_print = "expected_do.txt"

        with open(exp_json, "r") as f:
            TestCommandPrint.word_exp_json = json.load(f)

        with open(exp_print, "r") as f:
            TestCommandPrint.word_exp_print = f.read()

        os.makedirs(TestCommandPrint.dir_path, exist_ok=True)
        shutil.copy(exp_json, os.path.join(TestCommandPrint.dir_path, "do.json"))

    @classmethod
    def tearDownClass(cls):
        # shutil.rmtree(TestCommandPrint.dir_path)
        pass

    def setUp(self):
        self.word = "do"
        self.DIR_PATH = TestCommandPrint.dir_path

    @unittest.skip("SKIP ---- Have a lot to implement")
    def test_print_all(self):
        cmd = PrintCommand()

        text = cmd.execute(self.word)

        self.assertEqual(text, TestCommandPrint.word_exp_print)

    def test_print_opensCorrectFile(self):
        cmd = PrintCommand()
        cmd.set_dir_path(self.DIR_PATH)

        with patch.object(PrintCommand, "_json_to_text") as mock_totext:
            with patch("json.load") as mock_load:
                mock_load.return_value = TestCommandPrint.word_exp_json

                cmd.execute(self.word)

                mock_totext.assert_called_once_with(TestCommandPrint.word_exp_json)

    def test_printContent_callsAllToTextMethods(self):
        cmd = PrintCommand()

        with patch.object(PrintCommand, "_frequency_to_text") as mock_freq:
            with patch.object(PrintCommand, "_definitions_to_text") as mock_defs:
                with patch.object(PrintCommand, "_translations_to_text") as mock_trans:
                    with patch.object(PrintCommand, "_synonyms_to_text") as mock_syns:
                        with patch.object(PrintCommand, "_examples_to_text") as mock_ex:

                            cmd._json_to_text(TestCommandPrint.word_exp_json)

                            mock_freq.assert_called_once_with(mock.ANY)
                            mock_defs.assert_called_once_with(mock.ANY)
                            mock_trans.assert_called_once_with(mock.ANY)
                            mock_syns.assert_called_once_with(mock.ANY)
                            mock_ex.assert_called_once_with(mock.ANY)

    @unittest.skip("SKIP ---- not yet impl")
    def test_jsonToText_returnsAll(self):
        cmd = PrintCommand()

        text = cmd._json_to_text(TestCommandPrint.word_exp_json)

        self.assertEqual(text, TestCommandPrint.word_exp_print)

    def test_toText_frequency(self):
        cmd = PrintCommand()

        text = cmd._frequency_to_text(TestCommandPrint.word_exp_json)

        self.assertEqual(text, "[Extremely Common]\n\n")

    def test_toText_Definitions(self):
        cmd = PrintCommand()

        with patch.object(PrintCommand, "_read_gram_groups") as mock_ggroups:
            mock_ggroups.side_effect = ["group1\n", "group2\n", "group3\n", "group4\n", "group5\n"]

            text = cmd._definitions_to_text(TestCommandPrint.word_exp_json)

        self.assertEqual(text, "DEFINTIONS\n"
                               "group1\n"
                               "group2\n"
                               "group3\n"
                               "group4\n"
                               "group5\n\n")


if __name__ == "__main__":
    unittest.main()
