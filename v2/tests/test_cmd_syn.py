import unittest
from unittest import mock
from unittest.mock import patch, call

from src.input_processor import process_input, print_syn
from src.json_load import JsonLoader
from src.json_print import JsonPrinter


class SynCmdTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_syn_do_callsPrinterWithSyn(self):
        """
        input: string "syn(do)"
        expected result: call a "syn_print" function with "do" as parameter.
                         it doesn't matter what the printing does.
        assume: the do.syn file exists
        """

        with patch.object(JsonPrinter, 'print_syn') as mock_print_syn:
            process_input("syn(do)")

        mock_print_syn.assert_called_once_with(mock.ANY)

    def test_print_syn_printsContentForWord(self):
        syn_content = "dummy_content"

        with patch.object(JsonLoader, 'load') as mock_load:
            mock_load.return_value = syn_content
            with patch.object(JsonPrinter, 'print_syn') as mock_print:
                print_syn("do")

        mock_print.assert_called_once_with(syn_content)


if __name__ == '__main__':
    unittest.main()
