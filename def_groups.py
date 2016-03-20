from dict_parse import DictParser, DictSynParser
from etree_printer import *
import re

"""class WordFrequencyGroup:
    def __init__(self, etree_parent):
        self.etree_parent = etree_parent
        self.word_frequency = ""

    def translate(self):
        return {"word_frequency": ""}


# JSON: {"word": [...]};
class MainDefGroup:
    def __init__(self, etree_elem):
        self.etree_elem = etree_elem
        self.def_groups = []
        self.word_frequency = WordFrequencyGroup(etree_elem)

        # self.word.append({"word_frequency": ""})
        # self.word.append({"def_groups": []})
        # self.word.append({"examples": []})
        # self.word.append({"related_terms": []})
        # self.word.append({"nearby_words": []})
        # self.word.append({"synonyms": []})
        # self.word.append({"phrases": []})

    def translate_child(self, field):
        field_obj = getattr(self, field)
        if field_obj is self.word_frequency:
            return field_obj.translate()

        return None

    def translate(self):
        dict = {'word': []}
        return dict

        # if len(self.word_frequency):
#             dict.append(self.word_frequency)
#         if len(self.def_groups):
#             dict.append(self.def_groups)
#
#         return dict"""


class JsonGroup:
    def __init__(self, dict_parser: DictParser):
        self.dict_parser = dict_parser

    def translate(self) -> dict:
        pass


class WordFrequencyGroup(JsonGroup):
    def __init__(self, dict_parser: DictParser):
        JsonGroup.__init__(self, dict_parser)
        self.word_freq = ''

    def build(self):
        freq_phrase = self.dict_parser.get_word_freq()
        self.word_freq = freq_phrase.partition(".")[0]

    def translate(self) -> dict:
        return self.word_freq


class DefSubgroup(JsonGroup):
    def __init__(self, dict_parser: DictParser, etree_elem):
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
    def __init__(self, dict_parser: DictParser, etree_elem):
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
    def __init__(self, dict_parser: DictParser, etree_elem):
        JsonGroup.__init__(self, dict_parser)
        self.etree_elem = etree_elem
        self.defs = []

    def build(self):
        sslist = self.dict_parser.get_senselist(self.etree_elem)
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
    def __init__(self, dict_parser: DictParser, etree_elem):
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
    def __init__(self, dict_parser: DictParser, etree_def_group):
        JsonGroup.__init__(self, dict_parser)
        self.etree_elem = etree_def_group
        self.name = ''
        self.semantics = None
        self.gram_groups = []
        self.related = None

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


"""class RelatedTermsGroup(JsonGroup):
    def __init__(self, dict_parser):
        JsonGroup.__init__(self, dict_parser)
        self.terms = []

    def build(self):
        # self.terms = self.dict_parser.get_all_related_terms()
        pass

    def translate(self):
        children = []
        return {"related_terms": self.terms}"""


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


#####################################


class SynListGroup(JsonGroup):
    def __init__(self, dict_parser: DictSynParser, etree_elem):
        JsonGroup.__init__(self, dict_parser)
        self.etree_elem = etree_elem
        self.dict_parser = dict_parser
        self.list = []
        self.category = ""

    def build(self):
        self.list = self.dict_parser.get_synonyms(self.etree_elem)
        self.category = self.dict_parser.get_synonyms_category(self.etree_elem)

    def translate(self) -> dict:
        json_obj = {"line": self.list}

        if len(self.category):
            json_obj["category"] = self.category

        return json_obj


class SynSenseListGroup(JsonGroup):
    def __init__(self, dict_parser: DictSynParser, etree_elem):
        JsonGroup.__init__(self, dict_parser)
        self.etree_elem = etree_elem
        self.groups = []

    def build(self):
        sslist = self.dict_parser.get_senselist(self.etree_elem)
        sslitems = self.dict_parser.get_all_senselist_items(sslist)

        for item in sslitems:
            word_def = SynListGroup(self.dict_parser, item)
            word_def.build()
            self.groups.append(word_def)

    def translate(self) -> dict:
        json_children = []
        if len(self.groups):
            for group in self.groups:
                json_children.append(group.translate())

        return json_children


class SynGramGroup(JsonGroup):
    def __init__(self, dict_parser: DictSynParser, etree_elem):
        JsonGroup.__init__(self, dict_parser)
        self.etree_elem = etree_elem
        self.dict_parser = dict_parser
        self.grammar_value = None
        self.synonyms = None

    def build(self):
        self.grammar_value = self.dict_parser.get_gram_value(self.etree_elem)
        if len(self.grammar_value) == 0:
            self.grammar_value = None
        self.synonyms = SynSenseListGroup(self.dict_parser, self.etree_elem)
        self.synonyms.build()

    def translate(self) -> dict:
        json_object = {}
        if self.grammar_value is not None:
            json_object["value"] = self.grammar_value
        if self.synonyms is not None:
            json_object["synonyms"] = self.synonyms.translate()

        return {"gram_group": json_object}


# {"syn_group": 1, "items": []}
class SynGroup(JsonGroup):
    def __init__(self, dict_parser: DictSynParser, etree_def_group):
        JsonGroup.__init__(self, dict_parser)
        self.etree_elem = etree_def_group
        self.name = ''
        self.gram_groups = []

        self.word = dict_parser.get_word_form_for_def_group(etree_def_group)

    def build(self):
        gram_groups = self.dict_parser.get_all_grammar_groups(self.etree_elem)
        for etree_item in gram_groups:
            child = SynGramGroup(self.dict_parser, etree_item)
            child.build()
            self.gram_groups.append(child)

    def translate(self) -> dict:
        json_children = []
        for child in self.gram_groups:
            json_child = child.translate()
            if json_child is not None:
                json_children.append(json_child)

        if len(self.word):
            return {"word": self.word, "gram_groups": json_children}
        return None
