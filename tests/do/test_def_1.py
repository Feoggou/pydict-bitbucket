import unittest

from src.html_parser.def_parser import DefParser
from lxml import etree
from src.html_parser.etree_printer import *


class TestParser(unittest.TestCase):
    root = None

    @classmethod
    def setUpClass(cls):
        with open("def_1.html") as f:
            text = f.read()

        TestParser.root = etree.HTML(text)

    def setUp(self):
        self.sslist = TestParser.root.xpath('//body/ol')[0]
        self.d_parser = DefParser(TestParser.root, "do", fake=True)

    def assertElemKey(self, e, key):
        self.assertTrue(isinstance(e, etree._Element))
        self.assertIsNotNone(e)
        self.assertEqual(len(e.keys()), 1)
        found_key = e.keys()[0]

        self.assertEqual(found_key, key[0])
        self.assertEqual(e.get(found_key), key[1])

    def test_print_siblings(self):
        elem = self.sslist

        print_keys(elem, 0)
        print("keys: ", elem.keys())
        print("CHILDREN\n--------")

        """
        for child_elem in elem.getchildren():
            assert isinstance(child_elem, etree._Element)

            print_keys(child_elem, 0)
        """
        print_children(elem, 0)

    """ ---------------------- ACTUAL TESTS -------------------------"""

    def test_have_senselist_level1_from_gram_group(self):
        self.assertElemKey(self.sslist, ("class", "sense_list level_1"))

    def test_have_senselist_item_level1_from_gram_group(self):
        sslist_item = self.d_parser.get_senselist_item(self.sslist, "1")

        keys = sslist_item.keys()
        cls = keys[0], sslist_item.get(keys[0])
        value = keys[1], sslist_item.get(keys[1])

        self.assertEqual(value, ("value", "1"))
        self.assertEqual(cls, ("class", "sense_list_item level_1"))

    # FROM HERE ONWARD...

    def test_get_def_1_simple(self):
        sslist_item = self.d_parser.get_senselist_item(self.sslist, "1")

        word_def = self.d_parser.get_definition(sslist_item)

        self.assertEqual(word_def, "to bring to completion; finish")

    def test_get_category_from_sslist_item(self):
        sslist_item = self.d_parser.get_senselist_item(self.sslist, "2")

        word_categ = self.d_parser.get_definition_categ(sslist_item)

        self.assertEqual("informal", word_categ)

    def test_get_def_1_example_from_senselist_item(self):
        sslist_item = self.d_parser.get_senselist_item(self.sslist, "1")

        word_def = self.d_parser.get_def_example(sslist_item)

        self.assertEqual("dinner has been done for an hour", word_def)

    def test_get_def_3_with_links(self):
        sslist_item = self.d_parser.get_senselist_item(self.sslist, "3")

        word_def = self.d_parser.get_definition(sslist_item)

        self.assertEqual("a tributary stream opposed to effluent[1]noun, effluent (sense 2a)[1]", word_def)

    def test_get_def_style_listtype_SolomonBellows(self):
        sslist_item = self.d_parser.get_all_senselist_items(self.sslist)[3]

        word_def = self.d_parser.get_definition(sslist_item)

        self.assertEqual("Saul(born Solomon Bellows) 1915-2005; U.S. novelist, born in Canada", word_def)

    def test_get_def_4_beginsWithSpace(self):
        sslist_item = self.d_parser.get_senselist_item(self.sslist, "4")

        word_def = self.d_parser.get_definition(sslist_item)

        self.assertEqual("excrement; feces", word_def)


if __name__ == '__main__':
    unittest.main()
