import unittest
import os
import json
import shutil

from unittest import mock
from unittest.mock import patch

from src.cmd_print import PrintCommand
from src.json_reader import JsonReader

from src import colors


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
        exp_print = "expected_do2.txt"

        with open(exp_json, "r") as f:
            TestCommandPrint.word_exp_json = json.load(f)

        with open(exp_print, "r") as f:
            TestCommandPrint.word_exp_print = f.read()

        os.makedirs(TestCommandPrint.dir_path, exist_ok=True)
        shutil.copy(exp_json, os.path.join(TestCommandPrint.dir_path, "do.json"))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TestCommandPrint.dir_path)
        pass

    def setUp(self):
        self.word = "do"
        self.DIR_PATH = TestCommandPrint.dir_path

    def test_print_all(self):
        cmd = PrintCommand(self.word)
        cmd.set_dir_path(self.DIR_PATH)

        text = cmd.execute()
        text = text.replace(colors.RESET, "")
        text = text.replace(colors.RED, "")
        text = text.replace(colors.BOLDBLACK, "")
        text = text.replace(colors.BLUE, "")

        self.assertEqual(text, TestCommandPrint.word_exp_print)

    def test_print_opensCorrectFile(self):
        cmd = PrintCommand(self.word)
        cmd.set_dir_path(self.DIR_PATH)

        with patch.object(PrintCommand, "read_content") as mock_totext:
            with patch("json.load") as mock_load:
                mock_load.return_value = TestCommandPrint.word_exp_json

                cmd.execute()

                mock_totext.assert_called_once_with(TestCommandPrint.word_exp_json)


if __name__ == "__main__":
    unittest.main()
