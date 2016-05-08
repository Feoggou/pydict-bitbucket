import unittest
from src.html_parser.rel_parser import RelatedParser
from lxml import etree


class TestRelatedParser(unittest.TestCase):
    root = None

    @classmethod
    def setUpClass(cls):
        f = open("do_related.html")
        text = f.read()
        TestRelatedParser.root = etree.HTML(text)

    def setUp(self):
        self.parser = RelatedParser(TestRelatedParser.root)

    def test_have_item_columns(self):
        columns_etree = self.parser.get_def_main()
        assert isinstance(columns_etree, etree._Element)

        key = columns_etree.keys()[0]
        value = columns_etree.get(key)

        self.assertEqual((key, value), ("class", "columns"))

    def test_get_all_related_words(self):
        items = self.parser.get_all_related_words()

        self.assertEqual(items, [
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
