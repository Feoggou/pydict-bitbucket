# from lxml import etree
from .def_groups import *
from .def_parser import *
from .syn_parser import *
from .rel_parser import *


# SYNONYMS
class MainDefGroupSyn:
    def __init__(self, dict_parser: SynParser):
        self.dict_parser = dict_parser
        self.etree_main = self.dict_parser.get_def_main()
        self.syn_groups = []

    def build_children(self):
        groups = self.dict_parser.get_all_def_groups()
        for g in groups:
            item = SynGroup(self.dict_parser, g)
            item.build()
            self.syn_groups.append(item)

    def translate(self):
        json_children = []
        for x in self.syn_groups:
            json_children.append(x.translate())

        return json_children


# RELATED
class MainDefGroupRel:
    def __init__(self, dict_parser: RelatedParser):
        self.dict_parser = dict_parser
        self.etree_main = self.dict_parser.get_def_main()
        self.related_words = []

    def build_children(self):
        self.related_words = self.dict_parser.get_all_related_words()

    def translate(self):
        return self.related_words


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


class HtmlToJsonRelated:
    def __init__(self, html_content):
        self.html_content = html_content
        self.translated_obj = None

    def translate(self):
        root = etree.HTML(self.html_content)
        dict_parser = RelatedParser(root)

        main_def = MainDefGroupRel(dict_parser)
        main_def.build_children()
        self.translated_obj = main_def.translate()
        return self.translated_obj


class HtmlToJsonSynonyms:
    def __init__(self, word_name, html_content):
        self.word_name = word_name
        self.html_content = html_content
        self.translated_obj = None

    def translate(self):
        root = etree.HTML(self.html_content)
        dict_parser = SynParser(root, self.word_name)

        main_def = MainDefGroupSyn(dict_parser)
        main_def.build_children()
        self.translated_obj = main_def.translate()
        return self.translated_obj
