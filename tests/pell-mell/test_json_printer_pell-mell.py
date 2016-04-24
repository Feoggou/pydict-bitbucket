import unittest
import filecmp
import os
from src.cmd_print import PrintCommand
from src.cmd_nearby import PrintNearbyCommand


class JsonPrinterTest(unittest.TestCase):
    def setUp(self):
        self.word_name = "pell-mell"
        self.dir_path = "./test-data"

        self.expected_file = "expected_pell-mell.txt"

        if not os.path.isdir(self.dir_path):
            os.mkdir(self.dir_path)

    def test_defs_to_text(self):
        cmd = PrintCommand("expected_pell-mell", use_colors=False)
        cmd.set_dir_path(".")

        actual_text = cmd.execute()

        file_name = self.dir_path + "/pell-mell.txt"
        with open(file_name, "w") as f:
            f.write(actual_text)

        files_same = filecmp.cmp(file_name, self.expected_file, shallow=False)
        self.assertTrue(files_same)

        os.remove(file_name)

    def test_nearby_to_text(self):
        cmd = PrintNearbyCommand("expected_pell-mell")
        cmd.set_dir_path(".")

        actual_text = cmd.execute()

        file_name = self.dir_path + "/pell-mell_nby.txt"
        with open(file_name, "w") as f:
            f.write(actual_text)

        files_same = filecmp.cmp(file_name, "expected_pell-mell_nby.txt", shallow=False)
        self.assertTrue(files_same)

        os.remove(file_name)


if __name__ == '__main__':
    unittest.main()
