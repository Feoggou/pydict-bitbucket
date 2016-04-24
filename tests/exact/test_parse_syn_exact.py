import unittest
from src.html_parser.syn_parser import SynParser
from lxml import etree


class TestSynParser(unittest.TestCase):
    root = None

    @classmethod
    def setUpClass(cls):
        f = open("exact_syn.html")
        text = f.read()
        TestSynParser.root = etree.HTML(text)

    def setUp(self):
        self.parser = SynParser(TestSynParser.root, "exact")

    def assertElemKey(self, key, e):
        self.assertTrue(isinstance(e, etree._Element))
        self.assertIsNotNone(e)
        self.assertEqual(len(e.keys()), 1)
        found_key = e.keys()[0]

        self.assertEqual(found_key, key[0])
        self.assertEqual(e.get(found_key), key[1])

    def test_get_word_forms_for_def_group(self):
        def_groups = self.parser.get_all_def_groups()

        word_forms = []
        for dg in def_groups:
            word_form = self.parser.get_word_form_for_def_group(dg)
            word_forms.append(word_form)

        self.assertEqual(['exact'], word_forms)

    def test_get_all_def_groups(self):
        groups = self.parser.get_all_def_groups()

        self.assertElemKey(("id", "exact_1"), groups[0])
        self.assertEqual(len(groups), 1)

    def test_have_home_subsec(self):
        group = self.parser.get_all_def_groups()[0]
        elems = self.parser._get_all_home_subsecs(group)

        self.assertElemKey(("class", "similar-words hom-subsec"), elems[0])
        self.assertEqual(len(elems), 1)

        return elems

    def test_get_all_grammar_groups_for_first(self):
        def_group = self.parser.get_all_def_groups()[0]
        ggroups = self.parser.get_all_grammar_groups(def_group)
        self.assertEqual(2, len(ggroups))

        ggroup = ggroups[0]
        keys = ggroup.keys()
        id = keys[0], ggroup.get(keys[0])
        cls = keys[1], ggroup.get(keys[1])

        self.assertEqual(id, ("id", "exact_1.1"))
        self.assertEqual(cls, ("class", "hom"))

        for group in ggroups:
            keys = group.keys()
            cls = keys[1], group.get(keys[1])
            self.assertEqual(cls, ("class", "hom"))

    def test_get_all_gram_value_of_def_group(self):
        def_group = self.parser.get_all_def_groups()[0]

        gram_values = self.parser.get_all_grammar_values(def_group)
        self.assertEqual(["adjective", "verb"], gram_values)

    def test_get_gram_value_of_gram_group(self):
        def_group = self.parser.get_all_def_groups()[0]
        ggroup = self.parser.get_all_grammar_groups(def_group)[0]

        gram_value = self.parser.get_gram_value(ggroup)
        self.assertEqual("adjective", gram_value)

    def test_have_senselist_item_level1_from_gram_group(self):
        def_group = self.parser.get_all_def_groups()[0]
        ggroup = self.parser.get_all_grammar_groups(def_group)[0]
        assert isinstance(ggroup, etree._Element)

        sslist = self.parser.get_senselist(ggroup)
        sslist_item = self.parser.get_senselist_item(sslist, "1")

        keys = sslist_item.keys()
        cls = keys[0], sslist_item.get(keys[0])
        value = keys[1], sslist_item.get(keys[1])

        self.assertEqual(value, ("value", "1"))
        self.assertEqual(cls, ("class", "sense_list_item level_1"))

    def test_get_all_senselist_item_level1_from_gram_group_returns_1(self):
        def_group = self.parser.get_all_def_groups()[0]
        ggroup = self.parser.get_all_grammar_groups(def_group)[0]
        assert isinstance(ggroup, etree._Element)

        sslist = self.parser.get_senselist(ggroup)
        sslist_items = self.parser.get_all_senselist_items(sslist)
        self.assertEqual(len(sslist_items), 1)

    def test_get_synonyms_line_from_senselist_item(self):
        def_group = self.parser.get_all_def_groups()[0]
        ggroup = self.parser.get_all_grammar_groups(def_group)[0]
        assert isinstance(ggroup, etree._Element)

        sslist = self.parser.get_senselist(ggroup)
        sslist_item = self.parser.get_all_senselist_items(sslist)[0]

        synonyms = self.parser.get_synonyms(sslist_item)
        self.assertEqual(synonyms, [
            "accurate", "correct", "definite", "faultless", "precise", "right", "specific", "true", "unerring"
        ])


if __name__ == '__main__':
    unittest.main()
