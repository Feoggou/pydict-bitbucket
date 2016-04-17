import unittest
from src.json_seeker import *


class TestSeeker(unittest.TestCase):
    do_exp_content = None
    word_exp_content = None
    create_content = None

    @classmethod
    def setUpClass(cls):
        TestSeeker.do_exp_content = None

        exp_do = "./do/expected_do.json"
        exp_word = "word_json_read.json"
        create_word = "./search-tests-data/create.json"

        with open(exp_do, "r") as f:
            TestSeeker.do_exp_content = json.load(f)

        with open(exp_word, "r") as f:
            TestSeeker.word_exp_content = json.load(f)

        with open(create_word, "r") as f:
            TestSeeker.create_content = json.load(f)

    def setUp(self):
        # self.word = "do"
        self.dir_path = "./search-tests-data"

    def test_defs_searchContent_opensFileAndCallsToSearchContent(self):
        seeker = JsonSearch(self.dir_path, "play")

        # must: open file "do.json"
        # json.load info from it.
        # call json_search("play)
        # return: the list of defs.
        results = seeker.search_content("do.json")

        self.assertEqual(results, {"do.json": ["to produce or appear in (a play, etc.)", "to play the role of"]})

    def test_defs_searchJsonFindsItems(self):
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

    @unittest.skip("not yet ready!")
    def test_ex_searchContent_opensFileAndCallsToSearchContent(self):
        seeker = JsonSearch(self.dir_path, "create")

        # must: open file "create.json"
        # json.load info from it.
        # call json_search("play)
        # return: the list of defs.
        results = seeker.search_content("create.json")

        self.assertEqual(results, {"do.json": ["to produce or appear in (a play, etc.)", "to play the role of"]})

    def test_ex_searchJsonFindsItems(self):
        seeker = JsonSearch(self.dir_path, "create")

        # A. must search in:
        # 1. def_groups[i] / gram_groups[j] // examples[k]
        # 2. translations[i]
        # B. must sort & unique them
        # C. must find the items in A that contain word "play"

        result = seeker._search_json_ex(TestSeeker.create_content, "create")

        self.assertEqual(result, [
            "new industries create new jobs",
            "[transl.] To create something means to cause it to happen or exist.It is really great for a radio "
            "producer to create a show like this. creates, creating, created"])


if __name__ == '__main__':
    unittest.main()
