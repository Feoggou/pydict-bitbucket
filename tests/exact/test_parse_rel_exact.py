import unittest
from src.html_parser.rel_parser import RelatedParser
from lxml import etree


class TestRelatedParser(unittest.TestCase):
    root = None

    @classmethod
    def setUpClass(cls):
        f = open("exact_related.html")
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

        self.assertEqual(items, ["act"])


if __name__ == '__main__':
    unittest.main()
