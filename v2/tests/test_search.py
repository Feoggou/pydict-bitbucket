import unittest


# SEARCH: search as regular expression
# search in: words, derived forms, etc.
#           options: vb, vt, vi, noun, etc.
#           does not search into examples. for that, we will have an "examples()"
#           also, we will have a "mine()", "myex()", "mydefs()", etc.
#           when searching in synonyms, perhaps we should pick a def or smth - in learn?
#           searches regardless of "known" and "useful".
# TODO: wsearch will search word-based (i.e. pick all word forms, then start search with each)
#       TAG will search solely based on tag
class TestSearch(unittest.TestCase):
    def test_dummy(self):
        pass

if __name__ == '__main__':
    unittest.main()
