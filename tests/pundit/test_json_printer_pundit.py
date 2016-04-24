import unittest
import filecmp
import os
from src.cmds.cmd_print import PrintCommand


class JsonPrinterTest(unittest.TestCase):
    def setUp(self):
        self.word_name = "pundit"
        self.dir_path = "test-data"

        self.expected_file = "expected_pundit.txt"

        if not os.path.isdir(self.dir_path):
            os.mkdir(self.dir_path)

    def test_json_to_text(self):
        cmd = PrintCommand("expected_pundit", use_colors=False)
        cmd.set_dir_path(".")

        actual_text = cmd.execute()

        file_name = self.dir_path + "/pundit.txt"
        with open(file_name, "w") as f:
            f.write(actual_text)

        files_same = filecmp.cmp(file_name, self.expected_file, shallow=False)
        self.assertTrue(files_same)

        os.remove(file_name)


if __name__ == '__main__':
    unittest.main()
