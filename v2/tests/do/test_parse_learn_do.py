import unittest

from src.learn_parser import LearnParser
from lxml import etree
from src.etree_printer import *


class TestParser(unittest.TestCase):
    root = None

    @classmethod
    def setUpClass(cls):
        with open("do_defs.html") as f:
            text = f.read()

        TestParser.root = etree.HTML(text)

    def setUp(self):
        self.parser = LearnParser(TestParser.root, "do")

    def test_haveCobuildictionary(self):
        dictionary = self.parser.get_cobuild_dict()

        self.assertIsNotNone(dictionary)

    def test_getAllDefGroups(self):
        def_groups = self.parser.get_all_def_groups()

        self.assertEqual(4, len(def_groups))

    def test_getDefGroupText_0(self):
        def_group = self.parser.get_all_def_groups()[0]

        text = self.parser.get_def_group_text(def_group)

        self.assertEqual("do - auxiliary verb uses", text)

    def test_getDefGroupText_1(self):
        def_group = self.parser.get_all_def_groups()[1]

        text = self.parser.get_def_group_text(def_group)

        self.assertEqual("do - other verb uses", text)

    def test_getDefGroupText_2(self):
        def_group = self.parser.get_all_def_groups()[2]

        text = self.parser.get_def_group_text(def_group)

        self.assertEqual("do - noun uses", text)

    def test_getDefGroupText_3(self):
        def_group = self.parser.get_all_def_groups()[3]

        text = self.parser.get_def_group_text(def_group)

        self.assertEqual("do.", text)

    def test_geNote_for_defGroup0(self):
        def_group = self.parser.get_all_def_groups()[0]
        note_text = self.parser.get_note(def_group)
        self.assertEqual(
            "Do is used as an auxiliary with the simple present tense. Did is used as an auxiliary with the simple "
            "past tense. In spoken English, negative forms of do are often shortened, for example do not is shortened "
            "to don't and did not is shortened to didn't.", note_text)

    def test_getAllGrammarGroups_for_defGroup0(self):
        def_group = self.parser.get_all_def_groups()[0]
        ggroups = self.parser.get_all_grammar_groups(def_group)
        self.assertEqual(9, len(ggroups))

    def test_getAllGrammarGroups_for_defGroup1(self):
        def_group = self.parser.get_all_def_groups()[1]
        ggroups = self.parser.get_all_grammar_groups(def_group)
        self.assertEqual(23, len(ggroups))

    def test_getAllGrammarGroups_for_defGroup2(self):
        def_group = self.parser.get_all_def_groups()[2]
        ggroups = self.parser.get_all_grammar_groups(def_group)
        self.assertEqual(2, len(ggroups))

    def test_getAllGrammarGroups_for_defGroup3(self):
        def_group = self.parser.get_all_def_groups()[3]
        ggroups = self.parser.get_all_grammar_groups(def_group)
        self.assertEqual(1, len(ggroups))

    def test_getGramValue_for_gramGroup0_def0(self):
        def_group = self.parser.get_all_def_groups()[0]
        ggroup = self.parser.get_all_grammar_groups(def_group)[0]

        gram_value = self.parser.get_gram_value(ggroup)
        self.assertEqual("auxiliary verb", gram_value)

    def test_getGramValue_for_gramGroup0_def1(self):
        def_group = self.parser.get_all_def_groups()[1]
        ggroup = self.parser.get_all_grammar_groups(def_group)[0]

        gram_value = self.parser.get_gram_value(ggroup)
        self.assertEqual("verb", gram_value)

    def test_getGramValue_for_gramGroup1_def19(self):
        def_group = self.parser.get_all_def_groups()[1]
        ggroup = self.parser.get_all_grammar_groups(def_group)[19]

        gram_value = self.parser.get_gram_value(ggroup)
        self.assertEqual("", gram_value)

    def test_getWordForms_for_defDroup0(self):
        def_group = self.parser.get_all_def_groups()[0]

        gram_value = self.parser.get_word_forms(def_group)
        self.assertEqual(['does', 'doing', 'did', 'done'], gram_value)

    def test_getWordForms_for_defGroup1(self):
        def_group = self.parser.get_all_def_groups()[1]

        gram_value = self.parser.get_word_forms(def_group)
        self.assertEqual(['does', 'doing', 'did', 'done'], gram_value)

    def test_getWordForms_for_defGroup2(self):
        def_group = self.parser.get_all_def_groups()[2]

        gram_value = self.parser.get_word_forms(def_group)
        self.assertEqual(['dos'], gram_value)

    def test_getWordForms_for_defGroup3(self):
        def_group = self.parser.get_all_def_groups()[3]

        gram_value = self.parser.get_word_forms(def_group)
        self.assertEqual([], gram_value)

    def test_allGramGroupsHaveOneDefEach_defGroup0(self):
        def_group = self.parser.get_all_def_groups()[0]
        for ggroup in self.parser.get_all_grammar_groups(def_group):
            sslist_items = self.parser.get_all_sense_items(ggroup)
            self.assertEqual(len(sslist_items), 1)

    def test_allGramGroupsHaveOneDefEach_defGroup1(self):
        def_group = self.parser.get_all_def_groups()[1]
        for ggroup in self.parser.get_all_grammar_groups(def_group):
            sslist_items = self.parser.get_all_sense_items(ggroup)
            self.assertEqual(len(sslist_items), 1)

    def test_allGramGroupsHaveOneDefEach_defGroup2(self):
        def_group = self.parser.get_all_def_groups()[2]
        for ggroup in self.parser.get_all_grammar_groups(def_group):
            sslist_items = self.parser.get_all_sense_items(ggroup)
            self.assertEqual(len(sslist_items), 1)

    def test_allGramGroupsHaveOneDefEach_defGroup3(self):
        def_group = self.parser.get_all_def_groups()[3]
        for ggroup in self.parser.get_all_grammar_groups(def_group):
            sslist_items = self.parser.get_all_sense_items(ggroup)
            self.assertEqual(len(sslist_items), 1)

    def test_getDef0_fromDefGroup0(self):
        def_group = self.parser.get_all_def_groups()[0]
        ggroup = self.parser.get_all_grammar_groups(def_group)[0]
        assert isinstance(ggroup, etree._Element)

        sense = self.parser.get_all_sense_items(ggroup)[0]
        def_text = self.parser.get_sense_def(sense)

        self.assertEqual("Do is used to form the negative of main verbs, by putting 'not' after 'do' and before the "
                         "main verb in its infinitive form, that is the form without 'to'.", def_text)

    def test_getDef1_fromDefGroup1(self):
        def_group = self.parser.get_all_def_groups()[1]
        ggroup = self.parser.get_all_grammar_groups(def_group)[1]
        assert isinstance(ggroup, etree._Element)

        sense = self.parser.get_all_sense_items(ggroup)[0]
        def_text = self.parser.get_sense_def(sense)

        self.assertEqual("Do can be used to stand for any verb group, or to refer back to another verb group, "
                         "including one that was in a previous sentence.", def_text)

    def test_getDef0_fromDefGroup2(self):
        def_group = self.parser.get_all_def_groups()[2]
        ggroup = self.parser.get_all_grammar_groups(def_group)[0]
        assert isinstance(ggroup, etree._Element)

        sense = self.parser.get_all_sense_items(ggroup)[0]
        def_text = self.parser.get_sense_def(sense)

        self.assertEqual("A do is a party, dinner party, or other social event.", def_text)

    def test_getDef1_fromDefGroup2(self):
        def_group = self.parser.get_all_def_groups()[2]
        ggroup = self.parser.get_all_grammar_groups(def_group)[1]
        assert isinstance(ggroup, etree._Element)

        sense = self.parser.get_all_sense_items(ggroup)[0]
        def_text = self.parser.get_sense_def(sense)

        self.assertEqual(None, def_text)

    def test_getDef0_fromDefGroup3(self):
        def_group = self.parser.get_all_def_groups()[3]
        ggroup = self.parser.get_all_grammar_groups(def_group)[0]
        assert isinstance(ggroup, etree._Element)

        sense = self.parser.get_all_sense_items(ggroup)[0]
        def_text = self.parser.get_sense_def(sense)

        self.assertEqual("do. is an old-fashioned written abbreviation for ditto.", def_text)

    def test_getExFromDef0_defGroup0_gramGroup0(self):
        def_group = self.parser.get_all_def_groups()[0]
        ggroup = self.parser.get_all_grammar_groups(def_group)[0]
        assert isinstance(ggroup, etree._Element)

        sense = self.parser.get_all_sense_items(ggroup)[0]
        def_text = self.parser.get_sense_example(sense)

        self.assertEqual([
            "They don't want to work.", "I did not know Jamie had a knife.", "It doesn't matter if you win or lose."
        ], def_text)

    def test_getExFromDef5_defGroup0_gramGroup0(self):
        def_group = self.parser.get_all_def_groups()[0]
        ggroup = self.parser.get_all_grammar_groups(def_group)[5]
        assert isinstance(ggroup, etree._Element)

        sense = self.parser.get_all_sense_items(ggroup)[0]
        def_text = self.parser.get_sense_example(sense)

        self.assertEqual(["Veronica, I do understand.", "You did have a tape recorder with you."], def_text)

    def test_getExFromDef0_defGroup1_gramGroup0(self):
        def_group = self.parser.get_all_def_groups()[1]
        ggroup = self.parser.get_all_grammar_groups(def_group)[0]
        assert isinstance(ggroup, etree._Element)

        sense = self.parser.get_all_sense_items(ggroup)[0]
        def_text = self.parser.get_sense_example(sense)

        self.assertEqual([
            "I was trying to do some work.",
            "After lunch Elizabeth and I did the washing up.",
            "Dad does the garden.",
            "Let me do your hair."
        ], def_text)

    def test_getCateg_fromDef5_defGroup0(self):
        def_group = self.parser.get_all_def_groups()[0]
        ggroup = self.parser.get_all_grammar_groups(def_group)[5]
        assert isinstance(ggroup, etree._Element)

        sense = self.parser.get_all_sense_items(ggroup)[0]
        def_text = self.parser.get_sense_categ(sense)

        self.assertEqual("emphasis", def_text)

    def test_getCategMultiple_fromDef0_defGroup2(self):
        def_group = self.parser.get_all_def_groups()[2]
        ggroup = self.parser.get_all_grammar_groups(def_group)[0]
        assert isinstance(ggroup, etree._Element)

        sense = self.parser.get_all_sense_items(ggroup)[0]
        def_text = self.parser.get_sense_categ(sense)

        self.assertEqual("mainly British, informal", def_text)


if __name__ == '__main__':
    unittest.main()
