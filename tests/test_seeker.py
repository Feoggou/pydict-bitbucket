import unittest
from src.json_seeker import *


class TestSeeker(unittest.TestCase):
    do_exp_content = None
    word_exp_content = None

    @classmethod
    def setUpClass(cls):
        TestSeeker.do_exp_content = None

        exp_do = "./do/expected_do.json"
        exp_word = "word_json_read.json"

        with open(exp_do, "r") as f:
            TestSeeker.do_exp_content = json.load(f)

        with open(exp_word, "r") as f:
            TestSeeker.word_exp_content = json.load(f)

    def setUp(self):
        # self.word = "do"
        self.dir_path = "./search-tests-data"

    def test_searchContent_opensFileAndCallsToSearchContent(self):
        seeker = JsonSearch(self.dir_path, "play")

        # must: open file "do.json"
        # json.load info from it.
        # call json_search("play)
        # return: the list of defs.
        results = seeker._search_content("do.json", "play")

        self.assertEqual(results, {"do.json": ["to produce or appear in (a play, etc.)", "to play the role of"]})

    def test_searchJsonFindsItems(self):
        seeker = JsonSearch(self.dir_path, "play")

        # A. must search in:
        # 1. def_groups[i] / semantics
        # 2. def_groups[i] / gram_groups[j] // defs[k]
        # 3. translations[i]
        # B. must sort & unique them
        # C. must find the items in A that contain word "play"

        result = seeker._search_json(TestSeeker.do_exp_content, "play")

        self.assertEqual(result, ["to produce or appear in (a play, etc.)", "to play the role of"])

    def test_getSemantics_retrievesAll(self):
        seeker = JsonSearch(self.dir_path, "play")

        semantics = seeker._get_semantics(TestSeeker.word_exp_content)

        self.assertEqual(semantics, ["<semantics_content_here>"])

    def test_getDefs_retrievesAll(self):
        seeker = JsonSearch(self.dir_path, "play")

        defs = seeker._get_defs(TestSeeker.word_exp_content)

        self.assertEqual(len(defs), 30)

    def test_getTranslations_retrievesAll(self):
        seeker = JsonSearch(self.dir_path, "play")

        transls = seeker._get_translations(TestSeeker.word_exp_content)

        self.assertEqual(transls, ["[transl.] When you do something, you take some action or perform an activity or task.I was trying to do some work. done"])


if __name__ == '__main__':
    unittest.main()
