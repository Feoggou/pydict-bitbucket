import sys

print("sys path: ", sys.path)

import unittest
from src.dict_parse import DictParser
from lxml import etree
from ..src.etree_printer import *


class TestParser(unittest.TestCase):
    root = None

    @classmethod
    def setUpClass(cls):
        f = open("do_defs.html")
        text = f.read()
        TestParser.root = etree.HTML(text)

    def setUp(self):
        self.d_parser = DictParser(TestParser.root, "do")

    def assertElemKey(self, e, key):
        self.assertTrue(isinstance(e, etree._Element))
        self.assertIsNotNone(e)
        self.assertEqual(len(e.keys()), 1)
        found_key = e.keys()[0]

        self.assertEqual(found_key, key[0])
        self.assertEqual(e.get(found_key), key[1])

    def test_can_find_def_hom_subsec(self):
        print(TestParser.root)
        key = ("class", "definitions hom-subsec")
        e = self.root.xpath('//*[@class="definitions hom-subsec"]')[0]
        self.assertElemKey(e, key)

    def test_can_find_h2entry_of_parent(self):
        key = ("class", "definitions hom-subsec")
        e = self.root.xpath('//*[@class="definitions hom-subsec"]')[0]
        self.assertElemKey(e, key)

        h2entry_key = ("class", "h2_entry")
        e = e.xpath('//*[@class="h2_entry"]')[0]
        self.assertElemKey(e, h2entry_key)


    """
    lang="en"; xmlns:fb="http://ogp.me/ns/fb#"; xmlns:og="http://opengraphprotocol.org/schema/";    /
    0 KEYS: class="definition   hasCookiePolicy"    /
    1 KEYS: id="wrapper"    /
    2 KEYS: class="content english"     /
    3 KEYS: class="dictionary"  /
    4 KEYS: class="definition_wrapper english"  /
    5 KEYS: class="definition_main" /
    6 KEYS: class="definition_content col main_bar"
(OR)6 KEYS: class="definition_sidebar col side_bar"         -- word frequency; related terms & nearby words. (href="/dictionary/american/<word>/related")
    7 KEYS: id="<word>_1", then id="<word>_2", etc.


(OR)7 KEYS: id="examples_box"                               -- examples.
    8 KEYS: class="homograph-entry"
(OR)8 KEYS: id="synonyms_box"                               -- synonyms here: /dictionary/american-thesaurus/do
    9 KEYS: class="definitions hom-subsec"
(OR)9 KEYS: class="re hom-subsec"                           -- related
(OR)9 KEYS: class="phrase"                                  -- phrases / related
    10 KEYS: id="<word>_<i>.<j>"; class="hom"               -- i = prev do, j = who knows?
    11 KEYS: class="sense_list level_<k>"
(OR)11 KEYS: class="gramGrp h3_entry"                       -- grammar value (intransitive verb, noun, etc.)
(OR)11 KEYS: class="inflected_forms"                        -- word forms

    12 KEYS: class="sense_list_item level_<k>"; value="<m>";    -- definition number <m>
    possible child: class="lbl {register/geo/etc.}"             -- categ (KEYS: 13 or 15)

    SUBDEFINITIONS
        13 KEYS: class="sense_list level_<k+1>"                 -- possible, if subdefinition.
        14 KEYS: class="sense_list_item level_<k+1>"; value="n"     -- subdefinition <n>

    (SUB)DEFINITIONS
    13 / 15 KEYS: class="def"                               -- definition in TEXT
    13 / 15 KEYS: class="orth"                              -- example for current def.
    """

    def test_print_siblings(self):
        elem = self.root.xpath('//*[@class="gramGrp h3_entry"]')[0]

        print_keys(elem, 0)
        print("CHILDREN\n--------")

        # """
        for child_elem in elem.getchildren():
            assert isinstance(child_elem, etree._Element)

            print_keys(child_elem, 0)
        # """
        # print_children(elem, 0)

    """ ---------------------- ACTUAL TESTS -------------------------"""

    def test_frequency_is_correct(self):
        freq_phrase = self.d_parser.get_word_freq()
        word_freq = freq_phrase.partition(".")[0]

        self.assertEqual(word_freq, "Extremely Common")

    def test_get_all_examples(self):
        examples = self.d_parser.get_all_examples()

        self.assertEqual(examples[0],
            'You should write the general principles down somewhere, Dad, like they do with the United States Code.')

        self.assertEqual(len(examples), 1)

    def test_get_all_rel_words_from_def_group(self):
        def_group = self.d_parser.get_all_def_groups()[0]
        rel_words = self.d_parser.get_all_related_words(def_group)

        self.assertEqual(len(rel_words), 13)
        self.assertEqual(rel_words, ["do a deal", "do by", "do down", "do in", "do it", "do over", "do's and don'ts",
                                     "do up", "do up right", "do oneself well", "do with", "do without", "have to do with"])

    def test_get_all_nearby_words(self):
        nearby_words = self.d_parser.get_all_nearby_words()
        self.assertEqual(nearby_words[0], "Dn")
        self.assertEqual(len(nearby_words), 20)

    def test_get_def_main(self):
        print(TestParser.root)
        key = ("class", "definition_main")
        e = self.d_parser.get_def_main()
        self.assertElemKey(e, key)

    def test_have_5_def_groups(self):
        elems = self.d_parser.get_all_def_groups()
        key = ("id", "do_1")
        self.assertElemKey(elems[0], key)
        self.assertEqual(len(elems), 5)

    def test_get_all_grammar_groups_for_first(self):
        def_group = self.d_parser.get_all_def_groups()[0]
        ggroups = self.d_parser.get_all_grammar_groups(def_group)
        self.assertEqual(4, len(ggroups))

        ggroup = ggroups[0]
        keys = ggroup.keys()
        id = keys[0], ggroup.get(keys[0])
        cls = keys[1], ggroup.get(keys[1])

        self.assertEqual(id, ("id", "do_1.1"))
        self.assertEqual(cls, ("class", "hom"))

        for group in ggroups:
            keys = group.keys()
            if 0:
                id = keys[0], group.get(keys[0])
                print("id=", id)
            cls = keys[1], group.get(keys[1])
            self.assertEqual(cls, ("class", "hom"))

    def test_get_all_gram_value_of_def_group(self):
        def_group = self.d_parser.get_all_def_groups()[0]

        gram_values = self.d_parser.get_all_grammar_values(def_group)
        self.assertEqual(["transitive verb", "intransitive verb", "auxiliary verb", "noun"], gram_values)

    def test_get_gram_value_of_gram_group(self):
        def_group = self.d_parser.get_all_def_groups()[0]
        ggroup = self.d_parser.get_all_grammar_groups(def_group)[0]

        gram_value = self.d_parser.get_gram_value(ggroup)
        self.assertEqual("transitive verb", gram_value)

    def test_get_wordforms_for_gram_group(self):
        def_group = self.d_parser.get_all_def_groups()[0]
        ggroup = DictParser.get_all_grammar_groups(def_group)[0]

        gram_value = self.d_parser.get_word_forms(ggroup)
        self.assertEqual(['did', 'done', 'doing'], gram_value)

    def test_get_word_forms_for_def_group(self):
        def_groups = self.d_parser.get_all_def_groups()

        word_forms = []
        for dg in def_groups:
            word_form = self.d_parser.get_word_form_for_def_group(dg)
            word_forms.append(word_form)

        self.assertEqual(['do', 'do', 'do', 'Do or do', 'DO or D.O.'], word_forms)

    def test_have_senselist_level1_from_gram_group(self):
        def_group = self.d_parser.get_all_def_groups()[0]
        ggroup = self.d_parser.get_all_grammar_groups(def_group)[0]
        assert isinstance(ggroup, etree._Element)

        sslist = self.d_parser.get_senselist(ggroup)

        self.assertElemKey(sslist, ("class", "sense_list level_1"))

    def test_have_senselist_item_level1_from_gram_group(self):
        def_group = self.d_parser.get_all_def_groups()[0]
        ggroup = self.d_parser.get_all_grammar_groups(def_group)[0]
        assert isinstance(ggroup, etree._Element)

        sslist = self.d_parser.get_senselist(ggroup)
        sslist_item = self.d_parser.get_senselist_item(sslist, "2")

        keys = sslist_item.keys()
        cls = keys[0], sslist_item.get(keys[0])
        value = keys[1], sslist_item.get(keys[1])

        self.assertEqual(value, ("value", "2"))
        self.assertEqual(cls, ("class", "sense_list_item level_1"))

    def test_get_all_senselist_item_level1_from_gram_group_returns_22(self):
        def_group = self.d_parser.get_all_def_groups()[0]
        ggroup = self.d_parser.get_all_grammar_groups(def_group)[0]
        assert isinstance(ggroup, etree._Element)

        sslist = self.d_parser.get_senselist(ggroup)
        sslist_items = self.d_parser.get_all_senselist_items(sslist)
        self.assertEqual(len(sslist_items), 22)


    def test_get_def_from_senselist_item(self):
        def_group = self.d_parser.get_all_def_groups()[0]
        ggroup = self.d_parser.get_all_grammar_groups(def_group)[0]
        assert isinstance(ggroup, etree._Element)

        sslist = self.d_parser.get_senselist(ggroup)
        sslist_item = self.d_parser.get_senselist_item(sslist, "2")

        word_def = self.d_parser.get_definition(sslist_item)

        self.assertEqual(word_def, "to bring to completion; finish")

    def test_get_category_from_sslist_item(self):
        def_group = self.d_parser.get_all_def_groups()[1]
        ggroup = self.d_parser.get_all_grammar_groups(def_group)[0]
        assert isinstance(ggroup, etree._Element)

        sslist = self.d_parser.get_senselist(ggroup)
        sslist_item = self.d_parser.get_all_senselist_items(sslist)[0]

        word_categ = self.d_parser.get_definition_categ(sslist_item)

        self.assertEqual("music", word_categ)

    def test_get_def_example_from_senselist_item(self):
        def_group = self.d_parser.get_all_def_groups()[0]
        ggroup = self.d_parser.get_all_grammar_groups(def_group)[0]
        assert isinstance(ggroup, etree._Element)

        sslist = self.d_parser.get_senselist(ggroup)
        sslist_item = self.d_parser.get_senselist_item(sslist, "3")

        word_def = self.d_parser.get_def_example(sslist_item)

        print("word_def='{}'".format(word_def))

        self.assertEqual("it does no harm; who did this to you?", word_def)

    def test_get_related_words(self):
        # self.fail()
        pass

    def test_get_synonyms(self):
        # self.fail()
        pass

    """def test_DictElem_to_json(self):
        de = DefinitionElem("text")
        s = json.dumps(de.__dict__)
        print("dict=", de.__dict__)"""


# key: class="definitions hom-subsec"
#   key: class="h2_entry"
#       key: class="pos" --- i.e. grammar value (e.g. noun)
#       key: class="inflected_forms" --- has word forms
#       key: class="sense_list level_<n>"; value="n"; ---- 1.a, 1.b, 2.a, etc.
#          key: class="def"     --- word definition
#               key: class="hi"     --- word example (in 'class="orth"' --- there may be many)


if __name__ == '__main__':
    unittest.main()