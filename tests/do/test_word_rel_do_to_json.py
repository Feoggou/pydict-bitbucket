import unittest
from src.html_parser.rel_groups import *


# {"related_words": []},
class HtmlToJsonRelTest(unittest.TestCase):
    def setUp(self):
        f = open("do_related.html")
        self.html_content = f.read()
        self.maxDiff = None

    def test_create_html_to_json_obj(self):
        obj = HtmlToJsonRelated(self.html_content)
        self.assertIsNotNone(obj)

    def test_translate_main_to_json_returns_all_related_words(self):
        obj = HtmlToJsonRelated(self.html_content)
        json_obj = obj.translate()
        self.assertEqual(json_obj, [
            "do by", "do up", "do down", "do time", "make do", "do-gooder", "do penance", "do-or-die", "do honor to",
            "do up right", "whoop-de-do", "do credit to", "do the honors", "do oneself well", "do-it-yourself",
            "do one's (or its) business", "have to do with", "Mato Grosso do Sul", "do in", "to-do", "do gree",
            "do with", "do-si-do", "derring-do", "do without", "how-do-you-do", "do to death", "tae kwon do",
            "How do you do?", "do justice to", "do the trick", "do someone dirt", "do a number on", "do oneself justice",
            "do one's damnedest (or damndest)", "Rio Grande do Norte", "do it", "can-do", "do over", "do-rag",
            "do tell!", "do a deal", "do-nothing", "do duty for", "do up brown", "well-to-do", "do away with",
            "do one's bit", "ne'er-do-well", "do wonders for", "do business with", "do oneself proud",
            "do the bidding of", "Rio Grande do Sul"])

if __name__ == '__main__':
    unittest.main()
