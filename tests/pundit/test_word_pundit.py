import unittest
from unittest.mock import patch
import os
from src import word
import json
import filecmp


class WordTest(unittest.TestCase):
    count = 0

    def setUp(self):
        self.word_name = "pundit"
        self.dir_path = "./test-data"

        self.base_file_name = self.dir_path + "/" + self.word_name
        self.expected_file = "expected_pundit.json"

        if not os.path.isdir(self.dir_path):
            os.mkdir(self.dir_path)

        # self.maxDiff = None

    def _gen_unique_filename(self) -> str:
        file_name = "{}-{}.json".format(self.base_file_name, str(WordTest.count))
        WordTest.count += 1
        return file_name

    @patch('src.word.WordData.fetch', word.WordData.fetch_mock)
    def test_get_word_contents_using_mock(self):
        word_data = word.WordData(self.word_name)
        word_data.fetch()

        self.assertEqual(word_data.word_name, self.word_name)

        self.assertGreater(len(word_data.def_content), 0)
        self.assertGreater(len(word_data.related_content), 0)
        self.assertEqual(len(word_data.synonyms_content), 0)

    @patch('src.word.WordData.fetch', word.WordData.fetch_mock)
    def test_json_result(self):
        word_data = word.WordData(self.word_name)
        word_data.fetch()

        content = word_data.build_content()
        file_name = self._gen_unique_filename()

        with open(file_name, "w") as f:
            json.dump(content, f, indent=4, sort_keys=True)

        files_same = filecmp.cmp(file_name, self.expected_file, shallow=False)
        self.assertTrue(files_same)

        os.remove(file_name)

    def test_json_result_with_real_download(self):
        word_data = word.WordData(self.word_name)
        word_data.fetch()

        content = word_data.build_content()
        file_name = self._gen_unique_filename()
        print("test_json_result_with_real_download uses: ", file_name)

        with open(file_name, "w") as f:
            json.dump(content, f, indent=4, sort_keys=True)

        files_same = filecmp.cmp(file_name, self.expected_file, shallow=False)
        self.assertTrue(files_same)

        os.remove(file_name)

    def test_download_html(self):
        """word_data = word.WordData(self.word_name)
        text = word_data.download_definition()

        f = open(self.base_file_name + "_downloaded.htm", "w")
        f.write(text)"""
        # TODO: use printer to write etree keys into .keys file, then search the "phrases" and see what changed.
        pass

    def tearDown(self):
        pass
        # os.rmdir(self.dir_path)
        # shutil.rmtree(self.dir_path)


if __name__ == '__main__':
    unittest.main()
