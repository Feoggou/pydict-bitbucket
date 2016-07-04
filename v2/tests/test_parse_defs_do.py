import unittest
import os

from src.def_parser import DefParser
from lxml import etree
from src.etree_printer import *


class TestParser(unittest.TestCase):
    root = None

    @classmethod
    def setUpClass(cls):
        path = os.path.dirname(os.path.abspath(__file__))
        file_name = os.path.join(path, "html_files", "do_defs.html")

        with open(file_name) as f:
            text = f.read()

        TestParser.root = etree.HTML(text)

    def setUp(self):
        self.parser = DefParser(TestParser.root, "do")

    def test_print_siblings(self):
        """elem = self.root.xpath(
            '/html/body/main/div[@class="dictionary"]/'                     # 2
            'div[@class="res_cell_center"]/'                                # 3
            'div[@class="definition_content res_cell_center_content"]/'     # 4
            'div[@id="do_1"]/'                                              # 5
            'div[@class="homograph-entry"]/'                                # 6
            'div[@class=" page"]/'                                          # 7
            'div[@class="dictionary dictionaries"]/'                        # 8
            'div[@class="Collins_Eng_Dict dictionary"]/'                    # 9
            'div[@class=" dictentry"]'                                      # 10
        )[0]"""

        """# examples
        elem = self.root.xpath(
            '/html/body/main/div[@class="dictionary"]/'                     # 2
            'div[@class="res_cell_center"]/'                                # 3
            'div[@class="definition_content res_cell_center_content"]/'     # 4
            'div[@id="do_1"]/'                                              # 5
            'div[@class="homograph-entry"]/'                                # 6
            'div[@class=" page"]/'                                          # 7
            'span[@class=" assets"]/'                        # 8
            'span[@class="Corpus_Examples_EN asset"]/'
            'span[@class=" assetlink"]/'
            'span[@class=" examples"]/'
            'div[@class="content examples"]/'
            'span[@class=" cit" and @type="example"]/'
            'span[@class=" quote"]'
        )[0]"""

        # def group header
        elem = self.root.xpath(
            '/html/body/main/div[@class="dictionary"]/'                     # 2
            'div[@class="res_cell_center"]/'                                # 3
            'div[@class="definition_content res_cell_center_content"]/'     # 4
            'div[@id="do_1"]/'                                              # 5
            'div[@class="homograph-entry"]/'                                # 6
            'div[@class=" page"]/'                                          # 7
            'div[@class="dictionary dictionaries"]/'                        # 8
            'div[@class="Collins_Eng_Dict dictionary"]/'                    # 9
            'div[@class=" dictentry"]/'                                     # 10
            'div[@class=" dictlink"]/'
            'div[@class="ced entry"]/'
            'div[@class="entry_header"]/'
            'h1[@class="h1_entry"]/'
            'span[@class=" orth"]'
        )[0]

        # print("ELEM TAG: ", elem.tag)

        print_keys(elem, 0)
        print("CHILDREN\n--------")

        # """
        for child_elem in elem.getchildren():
            assert isinstance(child_elem, etree._Element)

            print_keys(child_elem, 0)
        # """
        # print_children(elem, 0)

    """ ---------------------- ACTUAL TESTS -------------------------"""

    def test_haveCollinsDictionary(self):
        dictionary = self.parser.get_collins_dict()

        self.assertIsNotNone(dictionary)

    def test_getAllDefGroups(self):
        def_groups = self.parser.get_all_def_groups()

        self.assertEqual(6, len(def_groups))

    def test_getDefGroupText_0(self):
        def_group = self.parser.get_all_def_groups()[0]

        text = self.parser.get_def_group_text(def_group)

        self.assertEqual("do", text)

    def test_getDefGroupText_1(self):
        def_group = self.parser.get_all_def_groups()[1]

        text = self.parser.get_def_group_text(def_group)

        self.assertEqual("do or do a", text)

    def test_getDefGroupText_2(self):
        def_group = self.parser.get_all_def_groups()[2]

        text = self.parser.get_def_group_text(def_group)

        self.assertEqual("do", text)

    def test_getDefGroupText_3(self):
        def_group = self.parser.get_all_def_groups()[3]

        text = self.parser.get_def_group_text(def_group)

        self.assertEqual("do", text)

    def test_getDefGroupText_4(self):
        def_group = self.parser.get_all_def_groups()[4]

        text = self.parser.get_def_group_text(def_group)

        self.assertEqual("DO", text)

    def test_getDefGroupText_5(self):
        def_group = self.parser.get_all_def_groups()[5]

        text = self.parser.get_def_group_text(def_group)

        self.assertEqual("do.", text)

    def test_frequencyIsCorrect(self):
        first_def_group = self.parser.get_all_def_groups()[0]
        word_freq = self.parser.get_word_freq(first_def_group)

        self.assertEqual(word_freq, "Extremely Common")

    def test_getAllExamples(self):
        examples = self.parser.get_all_examples()

        self.assertEqual(
            examples, [
                "Then again, not to do him down too much, he does have his more positive side.",
                "I'd shouted: You want her to be French, do n't you, you can't stand the idea of Jessica being English!",
                "He was accusing me of being complicit in a murder, or being a murderer, I do n't know which.",
                "\"You should write the general principles down somewhere, Dad, like they do with the United States Code."
            ]
        )

    def test_getAllGrammarGroups_for_defGroup0(self):
        def_group = self.parser.get_all_def_groups()[0]
        ggroups = self.parser.get_all_grammar_groups(def_group)
        self.assertEqual(2, len(ggroups))

    def test_getGramValue_for_gramGroup0(self):
        def_group = self.parser.get_all_def_groups()[0]
        ggroup = self.parser.get_all_grammar_groups(def_group)[0]

        gram_value = self.parser.get_gram_value(ggroup)
        self.assertEqual("verb", gram_value)

    def test_getGramValue_for_gramGroup1(self):
        def_group = self.parser.get_all_def_groups()[0]
        ggroup = self.parser.get_all_grammar_groups(def_group)[1]

        gram_value = self.parser.get_gram_value(ggroup)
        self.assertEqual("noun", gram_value)

    def test_getWordForms_for_defDroup0_gramDroup0(self):
        def_group = self.parser.get_all_def_groups()[0]
        ggroup = self.parser.get_all_grammar_groups(def_group)[0]

        gram_value = self.parser.get_word_forms(ggroup)
        self.assertEqual(['does', 'doing', 'did', 'done'], gram_value)

    def test_getWordForms_for_defGroup0_gramGroup1(self):
        def_group = self.parser.get_all_def_groups()[0]
        ggroup = self.parser.get_all_grammar_groups(def_group)[1]

        gram_value = self.parser.get_word_forms(ggroup)
        self.assertEqual(['dos', 'do\'s'], gram_value)

    def test_getWordFormsInfo_for_defGroup0_gramGroup0(self):
        def_group = self.parser.get_all_def_groups()[0]
        ggroup = self.parser.get_all_grammar_groups(def_group)[0]

        gram_value = self.parser.get_word_forms_info(ggroup)
        self.assertEqual("", gram_value)

    def test_getWordFormsInfo_for_defGroup0_gramGroup1(self):
        def_group = self.parser.get_all_def_groups()[0]
        ggroup = self.parser.get_all_grammar_groups(def_group)[1]

        gram_value = self.parser.get_word_forms_info(ggroup)
        self.assertEqual("plural", gram_value)

    def test_getAllSenseItems_from_gramGroup_returns_37(self):
        def_group = self.parser.get_all_def_groups()[0]
        ggroup = self.parser.get_all_grammar_groups(def_group)[0]
        assert isinstance(ggroup, etree._Element)

        sslist_items = self.parser.get_all_sense_items(ggroup)
        self.assertEqual(len(sslist_items), 37)

    def test_getDef0_fromDefGroup0_gramGroup0(self):
        def_group = self.parser.get_all_def_groups()[0]
        ggroup = self.parser.get_all_grammar_groups(def_group)[0]
        assert isinstance(ggroup, etree._Element)

        sense = self.parser.get_all_sense_items(ggroup)[0]
        def_text = self.parser.get_sense_def(sense)

        self.assertEqual("to perform or complete (a deed or action)", def_text)

    def test_getDef33_fromDefGroup0_gramGroup0(self):
        def_group = self.parser.get_all_def_groups()[0]
        ggroup = self.parser.get_all_grammar_groups(def_group)[0]
        assert isinstance(ggroup, etree._Element)

        sense = self.parser.get_all_sense_items(ggroup)[33]
        def_text = self.parser.get_sense_def_label(sense)

        self.assertEqual("See do", def_text)

    def test_getDef35_fromDefGroup0_gramGroup0(self):
        def_group = self.parser.get_all_def_groups()[0]
        ggroup = self.parser.get_all_grammar_groups(def_group)[0]
        assert isinstance(ggroup, etree._Element)

        sense = self.parser.get_all_sense_items(ggroup)[35]
        def_text = self.parser.get_sense_def_label(sense)

        self.assertEqual("See how do you do?", def_text)

    def test_getDef25_fromDefGroup0_gramGroup0(self):
        def_group = self.parser.get_all_def_groups()[0]
        ggroup = self.parser.get_all_grammar_groups(def_group)[0]
        assert isinstance(ggroup, etree._Element)

        sense = self.parser.get_all_sense_items(ggroup)[25]
        def_text = self.parser.get_sense_def_label(sense)

        self.assertEqual("", def_text)

    def test_getEx0_fromDef0_defGroup0_gramGroup0(self):
        def_group = self.parser.get_all_def_groups()[0]
        ggroup = self.parser.get_all_grammar_groups(def_group)[0]
        assert isinstance(ggroup, etree._Element)

        sense = self.parser.get_all_sense_items(ggroup)[0]
        def_text = self.parser.get_sense_example(sense)

        self.assertEqual("to do a portrait; the work is done", def_text)

    def test_getUsage_fromDef1_defGroup0_gramGroup0(self):
        def_group = self.parser.get_all_def_groups()[0]
        ggroup = self.parser.get_all_grammar_groups(def_group)[0]
        assert isinstance(ggroup, etree._Element)

        sense = self.parser.get_all_sense_items(ggroup)[1]
        def_text = self.parser.get_sense_usage(sense)

        self.assertEqual("often intr; foll by for", def_text)

    def test_getCateg_fromDef21_defGroup0_gramGroup0(self):
        def_group = self.parser.get_all_def_groups()[0]
        ggroup = self.parser.get_all_grammar_groups(def_group)[0]
        assert isinstance(ggroup, etree._Element)

        sense = self.parser.get_all_sense_items(ggroup)[21]
        def_text = self.parser.get_sense_categ(sense)

        self.assertEqual("informal", def_text)

    def test_getCategMultiple_fromDef28_defGroup0_gramGroup0(self):
        def_group = self.parser.get_all_def_groups()[0]
        ggroup = self.parser.get_all_grammar_groups(def_group)[0]
        assert isinstance(ggroup, etree._Element)

        sense = self.parser.get_all_sense_items(ggroup)[28]
        def_text = self.parser.get_sense_categ(sense)

        self.assertEqual("Australian informal", def_text)

    def test_getCategMultiple_fromDef29_defGroup0_gramGroup0(self):
        def_group = self.parser.get_all_def_groups()[0]
        ggroup = self.parser.get_all_grammar_groups(def_group)[0]
        assert isinstance(ggroup, etree._Element)

        sense = self.parser.get_all_sense_items(ggroup)[29]
        def_text = self.parser.get_sense_categ(sense)

        self.assertEqual("slang, mainly British", def_text)

    def test_getOrigin(self):
        def_group = self.parser.get_all_def_groups()[0]

        result = self.parser.get_etymology(def_group)

        self.assertEqual("Old English dōn; related to Old Frisian duān, Old High German tuon, Latin abdere "
                         "to put away, Greek tithenai to place; see deed, doom", result)


if __name__ == '__main__':
    unittest.main()
