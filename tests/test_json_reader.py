import json
import os
import unittest
from unittest.mock import patch

from src.json_reader import *


class TestJsonReader(unittest.TestCase):
    content_text = None
    content_json = None
    dir_path = "./test-data"

    @classmethod
    def setUpClass(cls):
        TestJsonReader.expected_json = None
        TestJsonReader.expected_print = None

        exp_json = "word_json_read.json"
        exp_print = "word_json_read.txt"

        with open(exp_json, "r") as f:
            TestJsonReader.content_json = json.load(f)

        with open(exp_print, "r") as f:
            TestJsonReader.content_text = f.read()

        os.makedirs(TestJsonReader.dir_path, exist_ok=True)

    def setUp(self):
        self.word = "do"

    def test_toText_frequency(self):
        cmd = JsonReader(TestJsonReader.content_json)

        text = cmd.frequency()

        text = text.replace(colors.RESET, "")
        text = text.replace(colors.RED, "")
        text = text.replace(colors.BOLDBLACK, "")
        text = text.replace(colors.BLUE, "")

        self.assertEqual(text, "[Extremely Common]\n\n")

    def test_toText_examples(self):
        cmd = JsonReader(TestJsonReader.content_json)

        text = cmd.examples()

        text = text.replace(colors.RESET, "")
        text = text.replace(colors.RED, "")
        text = text.replace(colors.BOLDBLACK, "")
        text = text.replace(colors.BLUE, "")

        self.assertEqual(text,
                         "EXAMPLES\n"
                         "o) You should write the general principles down somewhere, "
                         "Dad, like they do with the United States Code.\n\n")

    def test_toText_translations(self):
        cmd = JsonReader(TestJsonReader.content_json)

        text = cmd.translations()

        text = text.replace(colors.RESET, "")
        text = text.replace(colors.RED, "")
        text = text.replace(colors.BOLDBLACK, "")
        text = text.replace(colors.BLUE, "")

        self.assertEqual(text, "TRANSLATIONS\n"
                               "When you do something, you take some action or perform an activity or task."
                               "I was trying to do some work. done\n\n\n")

    def test_toText_Definitions(self):
        cmd = JsonReader(TestJsonReader.content_json)

        with patch.object(DefGroupReader, "read_def_group") as mock_ggroups:
            mock_ggroups.side_effect = ["group1\n", "group2\n", "group3\n", "group4\n", "group5\n"]

            text = cmd.definitions()

            text = text.replace(colors.RESET, "")
            text = text.replace(colors.RED, "")
            text = text.replace(colors.BOLDBLACK, "")
            text = text.replace(colors.BLUE, "")

        self.assertEqual(text, "DEFINTIONS\n"
                               "group1\n"
                               "group2\n"
                               "group3\n"
                               "group4\n"
                               "group5\n"
                         )

    def test_toText_1stDefGroup(self):
        obj = TestJsonReader.content_json["def_groups"]
        reader = DefGroupReader(obj)

        with patch.object(GramGroupReader, "read_gram_group") as mock_ggroup:
            mock_ggroup.side_effect = ["ggroup1\n", "ggroup2\n", "ggroup3\n", "ggroup4\n"]

            text = reader.read_def_group(obj[0])

            text = text.replace(colors.RESET, "")
            text = text.replace(colors.RED, "")
            text = text.replace(colors.BOLDBLACK, "")
            text = text.replace(colors.BLUE, "")

        self.assertEqual(text,
                         "do\n"
                         "ggroup1\n"
                         "ggroup2\n"
                         "ggroup3\n"
                         "ggroup4\n\n"
                         "SEMANTICS\n"
                         "<semantics_content_here>\n\n"
                         "\n"
                         )

    def test_toText_1stGramGroup(self):
        obj = TestJsonReader.content_json["def_groups"][0]["gram_groups"]
        reader = GramGroupReader(obj)

        with patch.object(DefinitionReader, "read_definition") as mock_def:
            mock_def.side_effect = ["def1\n", "def2\n", "def3\n", "def4\n", "def5\n", "def6\n", "def7\n"]

            text = reader.read_gram_group(obj[0])

            text = text.replace(colors.RESET, "")
            text = text.replace(colors.RED, "")
            text = text.replace(colors.BOLDBLACK, "")
            text = text.replace(colors.BLUE, "")

        self.assertEqual(text,
                         "transitive verb\n"
                         "def1\n"
                         "def2\n"
                         "def3\n"
                         "def4\n"
                         "def5\n"
                         "def6\n"
                         "def7\n\n"
                         )

    def test_toText_definitionWithExample(self):
        obj = TestJsonReader.content_json["def_groups"][0]["gram_groups"][0]["defs"]
        reader = DefinitionReader(obj)

        text = reader.read_definition(obj[1])

        self.assertEqual(text,
                         "o) to bring to completion; finish\n"
                         "    e.g. dinner has been done for an hour\n"
                         )

    def test_toText_definitionWithCateg(self):
        obj = TestJsonReader.content_json["def_groups"][0]["gram_groups"][0]["defs"]
        reader = DefinitionReader(obj)

        text = reader.read_definition(obj[2])

        self.assertEqual(text,
                         "o) (informal) to bring about; cause; produce\n"
                         "    e.g. it does no harm; who did this to you?\n"
                         )

    def test_toText_defSubgroup(self):
        obj = TestJsonReader.content_json["def_groups"][0]["gram_groups"][0]["defs"]
        reader = DefinitionReader(obj)

        text = reader.read_definition(obj[0])

        self.assertEqual(text,
                         "o) \n"
                         "     to execute; effect; perform (an act, action, etc.)\n"
                         "         e.g. do great deeds\n"
                         "     to carry out; fulfill\n"
                         "         e.g. do what I tell you\n"
                         )

    def test_toText_defSubgroupWithCateg_full(self):
        obj = TestJsonReader.content_json["def_groups"][0]["gram_groups"][0]["defs"]
        reader = DefinitionReader(obj)

        text = reader.read_definition(obj[6])

        self.assertEqual(text,
                         "o) (informal) \n"
                         "     to prepare; cook\n"
                         "         e.g. that restaurant does ribs really well\n"
                         "     to eat\n"
                         "         e.g. let's do Mexican tonight\n"
                         )

    def test_toText_defSubgroup_subdefWithCated(self):
        obj = TestJsonReader.content_json["def_groups"][0]["gram_groups"][0]["defs"]
        reader = DefinitionReader(obj)

        text = reader.read_definition(obj[3])

        text = text.replace(colors.RESET, "")
        text = text.replace(colors.RED, "")
        text = text.replace(colors.BOLDBLACK, "")
        text = text.replace(colors.BLUE, "")

        self.assertEqual(text,
                         "o) \n"
                         "     to play the role of\n"
                         "         e.g. I did Polonius\n"
                         "     (informal) to imitate, or behave characteristically as\n"
                         "         e.g. to do a Houdini\n"
                         )

    def test_toText_Synonyms(self):
        cmd = JsonReader(TestJsonReader.content_json)

        with patch.object(SynGroupReader, "read_syn_group") as mock_ggroups:
            mock_ggroups.side_effect = ["group1\n"]

            text = cmd.synonyms()

            text = text.replace(colors.RESET, "")
            text = text.replace(colors.RED, "")
            text = text.replace(colors.BOLDBLACK, "")
            text = text.replace(colors.BLUE, "")

        self.assertEqual(text, "SYNONYMS\n"
                               "group1\n\n"
                         )

    def test_toText_1stSynDefGroup(self):
        obj = TestJsonReader.content_json["synonyms"]
        reader = SynGroupReader(obj)

        with patch.object(SynGramGroupReader, "read_gram_group") as mock_ggroup:
            mock_ggroup.side_effect = ["ggroup1\n", "ggroup2\n"]

            text = reader.read_syn_group(obj[0])

            text = text.replace(colors.RESET, "")
            text = text.replace(colors.RED, "")
            text = text.replace(colors.BOLDBLACK, "")
            text = text.replace(colors.BLUE, "")

        self.assertEqual(text,
                         "do\n"
                         "ggroup1\n"
                         "ggroup2\n"
                         )

    def test_toText_1stSynGramGroup(self):
        obj = TestJsonReader.content_json["synonyms"][0]["gram_groups"][0]["gram_group"]
        reader = SynGramGroupReader(obj)

        text = reader.read_gram_group(obj)

        text = text.replace(colors.RESET, "")
        text = text.replace(colors.RED, "")
        text = text.replace(colors.BOLDBLACK, "")
        text = text.replace(colors.BLUE, "")

        self.assertEqual(text,
                         "verb\n"
                         "o) perform, accomplish, achieve, carry out, complete, execute\n"
                         "o) be adequate, be sufficient, cut the mustard, pass muster, satisfy, suffice\n"
                         "o) get ready, arrange, fix, look after, prepare, see to\n"
                         "o) solve, decipher, decode, figure out, puzzle out, resolve, work out\n"
                         "o) cause, bring about, create, effect, produce\n\n"
                         )

    def test_jsonToText_readAll(self):
        cmd = JsonReader(TestJsonReader.content_json)

        text = cmd.read_content("do")

        text = text.replace(colors.RESET, "")
        text = text.replace(colors.RED, "")
        text = text.replace(colors.BOLDBLACK, "")
        text = text.replace(colors.BLUE, "")

        self.assertEqual(text, TestJsonReader.content_text)

if __name__ == "__main__":
    unittest.main()
