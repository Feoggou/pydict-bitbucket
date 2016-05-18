from .def_parser import DefParser
from lxml import etree


class JsonGroup:
    def __init__(self, dict_parser: DefParser):
        self.dict_parser = dict_parser

    def translate(self) -> dict:
        pass


class WordFrequencyGroup(JsonGroup):
    def __init__(self, dict_parser: DefParser):
        JsonGroup.__init__(self, dict_parser)
        self.word_freq = ''

    def build(self):
        self.word_freq = self.dict_parser.get_word_freq()

    def translate(self) -> dict:
        return self.word_freq


class DefSubgroup(JsonGroup):
    def __init__(self, dict_parser: DefParser, etree_elem):
        JsonGroup.__init__(self, dict_parser)
        self.subdefs = None
        self.etree_elem = etree_elem

    def build(self):
        self.subdefs = SenseListGroup(self.dict_parser, self.etree_elem)
        self.subdefs.build()

    def translate(self) -> dict:
        return {"def_subgroup": self.subdefs.translate()}


# {"category":"slang", "def":"excrement; feces", "example":"dog do"}
class WordDefinition(JsonGroup):
    def __init__(self, dict_parser: DefParser, etree_elem):
        JsonGroup.__init__(self, dict_parser)
        self.etree_elem = etree_elem
        self.category = ""
        self.definition = ""
        self.example = ""
        self.subgroup = None

    def build(self):
        sslist = self.dict_parser.get_senselist(self.etree_elem)
        if sslist is not None:
            self.subgroup = DefSubgroup(self.dict_parser, self.etree_elem)
            self.category = self.dict_parser.get_definition_categ(self.etree_elem)
            self.subgroup.build()
        else:
            self.definition = self.dict_parser.get_definition(self.etree_elem)
            self.category = self.dict_parser.get_definition_categ(self.etree_elem)
            self.example = self.dict_parser.get_def_example(self.etree_elem)

    def translate(self) -> dict:
        json_children = {}

        if self.subgroup is not None:
            json_children = self.subgroup.translate()
            if len(self.category):
                json_children["category"] = self.category

            return json_children
        else:
            if len(self.category):
                json_children["category"] = self.category
            json_children["def"] = self.definition
            if len(self.example):
                json_children["example"] = self.example

        return json_children


# {"defs": []}
# {"defs": [{"def": ""}, {"def": ""}, {"def": ""}]
class SenseListGroup(JsonGroup):
    def __init__(self, dict_parser: DefParser, etree_elem):
        JsonGroup.__init__(self, dict_parser)
        self.etree_elem = etree_elem
        self.defs = []

    def build(self):
        sslist = self.dict_parser.get_senselist(self.etree_elem)

        if sslist is None:
            word_def = WordDefinition(self.dict_parser, self.etree_elem)
            word_def.definition = self.dict_parser.get_alternative_def(self.etree_elem)
            self.defs.append(word_def)
            return

        sslitems = self.dict_parser.get_all_senselist_items(sslist)

        for item in sslitems:
            word_def = WordDefinition(self.dict_parser, item)
            word_def.build()
            self.defs.append(word_def)

    def translate(self) -> dict:
        json_children = []
        if len(self.defs):
            for word_def in self.defs:
                json_children.append(word_def.translate())

        return json_children


# {"gram_group": [{"word_forms": "did, done, doing"}, {"grammar_value": "transitive verb"}, {"defs": []}]}
class GramGroup(JsonGroup):
    def __init__(self, dict_parser: DefParser, etree_elem):
        JsonGroup.__init__(self, dict_parser)
        self.etree_elem = etree_elem
        self.word_forms = None
        self.grammar_value = None
        self.defs = None

    def build(self):
        self.word_forms = self.dict_parser.get_word_forms(self.etree_elem)
        if len(self.word_forms) == 0:
            self.word_forms = None

        self.grammar_value = self.dict_parser.get_gram_value(self.etree_elem)
        if len(self.grammar_value) == 0:
            self.grammar_value = None

        self.defs = SenseListGroup(self.dict_parser, self.etree_elem)
        self.defs.build()

    def translate(self) -> dict:
        json_object = {}
        if self.word_forms is not None:
            json_object["word_forms"] = self.word_forms
        if self.grammar_value is not None:
            json_object["value"] = self.grammar_value
        if self.defs is not None:
            json_object["defs"] = self.defs.translate()

        return json_object


# {"def_group": 1, "items": []}
class DefGroup(JsonGroup):
    def __init__(self, dict_parser: DefParser, etree_def_group):
        JsonGroup.__init__(self, dict_parser)
        self.etree_elem = etree_def_group
        self.name = ''
        self.semantics = None
        self.gram_groups = []
        self.related = None
        self.derived_forms = None

        self.word = dict_parser.get_word_form_for_def_group(etree_def_group)

    def build(self):
        gram_groups = self.dict_parser.get_all_grammar_groups(self.etree_elem)
        for etree_item in gram_groups:
            child = GramGroup(self.dict_parser, etree_item)
            child.build()
            self.gram_groups.append(child)

        self.related = RelatedGroup(self.dict_parser, self.etree_elem)
        self.related.build()

        self.semantics = self.dict_parser.get_semantics(self.etree_elem)
        self.derived_forms = self.dict_parser.get_all_derived_forms(self.etree_elem)

    def translate(self) -> dict:
        gram_groups = []
        for child in self.gram_groups:
            json_child = child.translate()
            if json_child is not None:
                gram_groups.append(json_child)

        json_obj = {"word": self.word, "gram_groups": gram_groups}

        if self.related is not None:
            related_children = self.related.translate()
            if len(related_children) > 0:
                json_obj["related"] = related_children

        if self.semantics is not None:
            json_obj["semantics"] = self.semantics

        if self.derived_forms is not None:
            json_obj["derived_forms"] = self.derived_forms

        if len(self.word):
            return json_obj
        return None


# {"def groups":[]}
class DefGroups(JsonGroup):
    def __init__(self, dict_parser):
        JsonGroup.__init__(self, dict_parser)
        self.children = []

    def build(self):
        etree_groups = self.dict_parser.get_all_def_groups()
        for etree_item in etree_groups:
            child = DefGroup(self.dict_parser, etree_item)
            child.build()
            self.children.append(child)

    def translate(self):
        json_children = []
        for child in self.children:
            json_child = child.translate()
            if json_child is not None:
                json_children.append(json_child)

        return json_children


class ExamplesGroup(JsonGroup):
    def __init__(self, dict_parser):
        JsonGroup.__init__(self, dict_parser)
        self.examples = []

    def build(self):
        examples = self.dict_parser.get_all_examples()
        for ex in examples:
            self.examples.append({"example": ex})

    def translate(self):
        return self.examples


class NearbyWordsGroup(JsonGroup):
    def __init__(self, dict_parser):
        JsonGroup.__init__(self, dict_parser)
        self.words = []

    def build(self):
        self.words = self.dict_parser.get_all_nearby_words()

    def translate(self):
        return self.words


class RelatedGroup(JsonGroup):
    def __init__(self, dict_parser, defgroup_etree):
        JsonGroup.__init__(self, dict_parser)
        self.defgroup_etree = defgroup_etree
        self.related = []

    def build(self):
        self.related = self.dict_parser.get_all_related_words(self.defgroup_etree)

    def translate(self):
        return self.related


class MainDefGroup:
    def __init__(self, dict_parser: DefParser):
        self.dict_parser = dict_parser
        self.etree_main = self.dict_parser.get_def_main()

        self.word_frequency = None
        self.def_groups = None
        self.examples = None
        self.nearby_words = None
        self.translations = None

    def build_children(self):
        self.word_frequency = WordFrequencyGroup(self.dict_parser)
        self.word_frequency.build()

        self.def_groups = DefGroups(self.dict_parser)
        self.def_groups.build()

        self.examples = ExamplesGroup(self.dict_parser)
        self.examples.build()

        self.nearby_words = NearbyWordsGroup(self.dict_parser)
        self.nearby_words.build()

        self.translations = self.dict_parser.get_all_translations()

    def translate(self):
        json_object = {}
        if self.word_frequency is not None:
            json_object["frequency"] = self.word_frequency.translate()
        if self.def_groups is not None:
            json_object["def_groups"] = self.def_groups.translate()
        if self.examples is not None:
            json_object["examples"] = self.examples.translate()
        if self.nearby_words is not None:
            json_object["nearby_words"] = self.nearby_words.translate()
        if self.translations is not None:
            json_object["translations"] = self.translations

        return json_object


class HtmlToJson:
    def __init__(self, word_name, html_content):
        self.word_name = word_name
        self.html_content = html_content
        self.translated_obj = None

    def translate(self):
        root = etree.HTML(self.html_content)
        dict_parser = DefParser(root, self.word_name)

        main_def = MainDefGroup(dict_parser)
        main_def.build_children()
        self.translated_obj = main_def.translate()
        return self.translated_obj

