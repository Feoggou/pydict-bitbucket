import unittest
from unittest.mock import patch
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
        seeker = JsonSearch(self.dir_path, "play", SearchIn.definitions)

        # must: open file "do.json"
        # json.load info from it.
        # call json_search("play)
        # return: the list of defs.
        results = seeker.search_content("do.json")

        self.assertEqual(results, {"do.json": ["to produce or appear in (a play, etc.)", "to play the role of"]})

    def test_defs_searchJsonFindsItems(self):
        seeker = JsonSearch(self.dir_path, "play", SearchIn.definitions)

        # A. must search in:
        # 1. def_groups[i] / semantics
        # 2. def_groups[i] / gram_groups[j] // defs[k]
        # 3. translations[i]
        # B. must sort & unique them
        # C. must find the items in A that contain word "play"

        result = seeker._search_json(TestSeeker.do_exp_content, "play")

        self.assertEqual(result, ["to produce or appear in (a play, etc.)", "to play the role of"])

    def test_getSemantics_retrievesAll(self):
        gatherer = ItemGatherer()

        semantics = gatherer._get_semantics(TestSeeker.word_exp_content)

        self.assertEqual(semantics, ["<semantics_content_here>"])

    def test_getDefs_retrievesAll(self):
        gatherer = ItemGatherer()

        defs = gatherer._get_defs(TestSeeker.word_exp_content)

        self.assertEqual(len(defs), 30)

    def test_getTranslations_retrievesAll(self):
        gatherer = ItemGatherer()

        transls = gatherer._get_translations(TestSeeker.word_exp_content)

        self.assertEqual(transls, ["[transl.] When you do something, you take some action or perform an activity or task.I was trying to do some work. done"])

    def test_ex_searchContent_opensFileAndCallsToSearchContent(self):
        seeker = JsonSearch(self.dir_path, "create", SearchIn.examples)

        # must: open file "create.json"
        # json.load info from it.
        # call json_search("play)
        # return: the list of defs.
        results = seeker.search_content("create.json")

        self.assertEqual(results, {"create.json": [
            "new industries create new jobs",
            "[transl.] To create something means to cause it to happen or exist.It is really great for a radio "
            "producer to create a show like this. creates, creating, created",
            'Two armchairs had been placed on top of it to create more floor-space.'
        ]})

    def test_ex_searchJsonFindsItems(self):
        seeker = JsonSearch(self.dir_path, "create", SearchIn.examples)

        # A. must search in:
        # 1. def_groups[i] / gram_groups[j] // examples[k]
        # 2. translations[i]
        # B. must sort & unique them
        # C. must find the items in A that contain word "play"

        result = seeker._search_json(TestSeeker.create_content, "create")

        self.assertEqual(result, [
            "new industries create new jobs",
            "[transl.] To create something means to cause it to happen or exist.It is really great for a radio "
            "producer to create a show like this. creates, creating, created",
            'Two armchairs had been placed on top of it to create more floor-space.'])

    def test_searchAll_searchFiles(self):
        seeker = JsonSearch(self.dir_path, "do", SearchIn.invalid)

        with patch.object(JsonSearch, "list_json_files") as mock_list:
            mock_list.return_value = ["a.json", "do.json", "doing.json", "b.json", "do-by.json"]

            results = seeker._search_files()

            self.assertEqual(results, ["do.json", "do-by.json"])


if __name__ == '__main__':
    unittest.main()
