import unittest
from unittest import mock
from unittest.mock import patch, call

from src.input_processor import process_input
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


if __name__ == '__main__':
    unittest.main()
