import unittest
import filecmp
import os
from src.json_printer import JsonPrinter


class JsonPrinterTest(unittest.TestCase):
    def setUp(self):
        self.word_name = "do"
        self.dir_path = "test-data"

        self.expected_file = "expected_do.txt"

        if not os.path.isdir(self.dir_path):
            os.mkdir(self.dir_path)

    def test_json_to_text(self):
        json_printer = JsonPrinter()
        text = json_printer.to_text("expected_do.json")

        file_name = self.dir_path + "/do.txt"
        with open(file_name, "w") as f:
            f.write(text)

        files_same = filecmp.cmp(file_name, self.expected_file, shallow=False)
        self.assertTrue(files_same)

        os.remove(file_name)


if __name__ == '__main__':
    unittest.main()
