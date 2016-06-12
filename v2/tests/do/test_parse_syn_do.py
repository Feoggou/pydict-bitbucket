import unittest

from src.syn_parser import SynParser
from lxml import etree
from src.etree_printer import *


class TestParser(unittest.TestCase):
    root = None

    @classmethod
    def setUpClass(cls):
        with open("do_syn.html") as f:
            text = f.read()

        TestParser.root = etree.HTML(text)

    def setUp(self):
        self.parser = SynParser(TestParser.root, "do")

    def test_getDefGroupText(self):
        text = self.parser.get_def_group_text()

        self.assertEqual("do", text)

    def test_getAllGrammarGroups_for_defGroup0(self):
        ggroups = self.parser.get_all_grammar_groups()
        self.assertEqual(2, len(ggroups))

    def test_getGramValue_for_gramGroup0(self):
        ggroup = self.parser.get_all_grammar_groups()[0]

        gram_value = self.parser.get_gram_value(ggroup)
        self.assertEqual("verb", gram_value)

    def test_getGramValue_for_gramGroup1(self):
        ggroup = self.parser.get_all_grammar_groups()[1]

        gram_value = self.parser.get_gram_value(ggroup)
        self.assertEqual("noun", gram_value)

    def test_getAllSenseItems_from_gramGroup_returns_37(self):
        ggroup = self.parser.get_all_grammar_groups()[0]
        assert isinstance(ggroup, etree._Element)

        sslist_items = self.parser.get_all_sense_items(ggroup)
        self.assertEqual(len(sslist_items), 17)

    def test_getSyns0_fromGramGroup0(self):
        ggroup = self.parser.get_all_grammar_groups()[0]
        assert isinstance(ggroup, etree._Element)

        sense = self.parser.get_all_sense_items(ggroup)[0]
        syn_list = self.parser.get_syn_line(sense)

        self.assertEqual({
            "perform": "", "work": "", "achieve": "", "carry out": "", "produce": "", "effect": "",
            "complete": "", "conclude": "", "undertake": "", "accomplish": "", "execute": "",
            "discharge": "", "pull off": "", "transact": ""
        }, syn_list)

    def test_getSyns8_fromGramGroup0(self):
        ggroup = self.parser.get_all_grammar_groups()[0]
        assert isinstance(ggroup, etree._Element)

        sense = self.parser.get_all_sense_items(ggroup)[8]
        syn_list = self.parser.get_syn_line(sense)

        self.assertEqual({
            "cheat": "informal", "trick": "", "con": "informal", "skin": "slang", "stiff": "slang", "sting": "informal",
            "deceive": "", "fleece": "", "hoax": "", "defraud": "", "dupe": "", "swindle": "", "diddle": "informal",
            "take (someone) for a ride": "informal", "pull a fast one on": "informal", "cozen": "", "scam": "slang"
        }, syn_list)

    def test_getSyns0_fromGramGroup1(self):
        ggroup = self.parser.get_all_grammar_groups()[1]
        assert isinstance(ggroup, etree._Element)

        sense = self.parser.get_all_sense_items(ggroup)[0]
        syn_list = self.parser.get_syn_line(sense)

        self.maxDiff = None

        self.assertEqual({
            "party": "informal, mainly British & New Zealand", "gathering": "", "function": "", "social": "",
            "event": "", "affair": "", "at-home": "", "occasion": "", "celebration": "", "reception": "",
            "bash": "informal", "rave": "British, slang", "get-together": "informal", "festivity": "",
            "knees-up": "British, informal", "beano": "British, slang", "social gathering": "", "shindig": "informal",
            "soirée": "", "rave-up": "British, slang", "hooley or hoolie": "mainly Irish & New Zealand"
        }, syn_list)

    def test_getEx0_fromDef0_defGroup0_gramGroup0(self):
        ggroup = self.parser.get_all_grammar_groups()[0]
        assert isinstance(ggroup, etree._Element)

        sense = self.parser.get_all_sense_items(ggroup)[0]
        def_text = self.parser.get_syn_example(sense)

        self.assertEqual("I was trying to do some work.", def_text)


if __name__ == '__main__':
    unittest.main()
