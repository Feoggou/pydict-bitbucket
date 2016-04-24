import unittest
from src.html_parser.rel_groups import *


# {"related_words": []},
class HtmlToJsonRelTest(unittest.TestCase):
    def setUp(self):
        f = open("affluent_related.html")
        self.html_content = f.read()
        self.maxDiff = None

    def test_create_html_to_json_obj(self):
        obj = HtmlToJsonRelated(self.html_content)
        self.assertIsNotNone(obj)

    def test_translate_main_to_json_returns_all_related_words(self):
        obj = HtmlToJsonRelated(self.html_content)
        json_obj = obj.translate()
        self.assertEqual(json_obj, [
            "effluent"])

if __name__ == '__main__':
    unittest.main()
