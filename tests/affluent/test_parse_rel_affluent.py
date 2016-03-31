import unittest
from src.rel_parser import RelatedParser
from lxml import etree


class TestRelatedParser(unittest.TestCase):
    root = None

    @classmethod
    def setUpClass(cls):
        f = open("affluent_related.html")
        text = f.read()
        TestRelatedParser.root = etree.HTML(text)

    def setUp(self):
        self.parser = RelatedParser(TestRelatedParser.root)

    def test_get_all_related_words(self):
        items = self.parser.get_all_related_words()

        self.assertEqual(items, [
            "effluent"])


if __name__ == '__main__':
    unittest.main()
