import unittest
import filecmp
import os
from src.json_printer import JsonPrinter


class JsonPrinterTest(unittest.TestCase):
    def setUp(self):
        self.word_name = "pell-mell"
        self.dir_path = "./test-data"

        self.expected_file = "expected_pell-mell.txt"

        if not os.path.isdir(self.dir_path):
            os.mkdir(self.dir_path)

    def test_defs_to_text(self):
        json_printer = JsonPrinter()
        text = json_printer.to_text("./expected_pell-mell.json")

        file_name = self.dir_path + "/pell-mell.txt"
        with open(file_name, "w") as f:
            f.write(text)

        files_same = filecmp.cmp(file_name, self.expected_file, shallow=False)
        self.assertTrue(files_same)

        os.remove(file_name)

    def test_nearby_to_text(self):
        json_printer = JsonPrinter()
        text = json_printer.nearby_to_text("./expected_pell-mell.json")
        expected_file = "expected_pell-mell_nby.txt"

        file_name = self.dir_path + "/pell-mell_nby.txt"
        with open(file_name, "w") as f:
            f.write(text)

        files_same = filecmp.cmp(file_name, expected_file, shallow=False)
        self.assertTrue(files_same)

        os.remove(file_name)


if __name__ == '__main__':
    unittest.main()
