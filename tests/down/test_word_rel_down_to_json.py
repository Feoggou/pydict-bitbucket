import unittest
from src.rel_groups import *


# {"related_words": []},
class HtmlToJsonRelTest(unittest.TestCase):
    def setUp(self):
        f = open("down_related.html")
        self.html_content = f.read()
        self.maxDiff = None

    def test_create_html_to_json_obj(self):
        obj = HtmlToJsonRelated(self.html_content)
        self.assertIsNotNone(obj)

    def test_translate_main_to_json_returns_all_related_words(self):
        obj = HtmlToJsonRelated(self.html_content)
        json_obj = obj.translate()
        self.assertEqual(json_obj, [
            "down-", "go down", "cut down", "lay down", "pay down", "put-down", "run-down", "sit-down", "bear down",
            "burn down", "come down", "Down East", "face down", "hold down", "hunt down", "mark down", "pipe down",
            "ride down", "do down", "bed down", "down-bow", "let down", "pin down", "rub down", "set down", "tie down",
            "beat down", "call down", "cool down", "down-home", "gear down", "howl down", "kick down", "melt down",
            "play down", "send down", "down on", "cry down", "get down", "mow down", "put down", "run down", "sit down",
            "back down", "boil down", "cast down", "cool-down", "dumb down", "hand down", "hull down", "live down",
            "nail down", "pull down", "shut down"])

if __name__ == '__main__':
    unittest.main()
