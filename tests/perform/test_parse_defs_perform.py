import unittest
from src.html_parser.def_parser import DefParser
from lxml import etree


class TestParser(unittest.TestCase):
    root = None

    @classmethod
    def setUpClass(cls):
        f = open("perform_defs.html")
        text = f.read()
        TestParser.root = etree.HTML(text)

    def setUp(self):
        self.d_parser = DefParser(TestParser.root, "perform")

    def assertElemKey(self, e, key):
        self.assertTrue(isinstance(e, etree._Element))
        self.assertIsNotNone(e)
        self.assertEqual(len(e.keys()), 1)
        found_key = e.keys()[0]

        self.assertEqual(found_key, key[0])
        self.assertEqual(e.get(found_key), key[1])


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
(OR)10 KEYS: class="semantic"                               -- explanations
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

    def test_get_semantic_explanation(self):
        def_group = self.d_parser.get_all_def_groups()[0]
        semantics = self.d_parser.get_semantics(def_group)

        # print(semantics)

        self.assertEqual(semantics,
            "perform, often a mere formal equivalent for do, is usually used of a more or less involved process "
            "rather than a single act [to perform an experiment ]; execute implies a putting into effect or completing "
            "that which has been planned or ordered [to execute a law ]; accomplish suggests effort and perseverance in "
            "carrying out a plan or purpose [to accomplish a mission ]; achieve implies the overcoming of obstacles in "
            "accomplishing something of worth or importance [to achieve a lasting peace ]; effect also suggests the "
            "conquering of difficulties but emphasizes what has been done to bring about the result [his cure was "
            "effected by the use of certain drugs ]; fulfill, in strict discrimination, implies the full realization of "
            "what is expected or demanded [to fulfill a promise ]")

    def test_get_derived_forms(self):
        def_group = self.d_parser.get_all_def_groups()[0]
        derived_forms = self.d_parser.get_all_derived_forms(def_group)

        self.assertEqual(derived_forms, {"adjective": "performable", "noun": "performer"})


if __name__ == '__main__':
    unittest.main()
