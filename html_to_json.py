from lxml import etree
from def_groups import *
from dict_parse import *


# SYNONYMS
class MainDefGroupSyn:
    def __init__(self, dict_parser: DictSynParser):
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
        json_children =  []
        for x in self.syn_groups:
            json_children.append(x.translate())

        return {'synonyms': json_children}


# RELATED
class MainDefGroupRel:
    def __init__(self, dict_parser: DictRelatedParser):
        self.dict_parser = dict_parser
        self.etree_main = self.dict_parser.get_def_main()
        self.related_words = []

    def build_children(self):
        self.related_words = self.dict_parser.get_all_related_words()

    def translate(self):
        return {'related_words': self.related_words}


class MainDefGroup:
    def __init__(self, dict_parser: DictParser):
        self.dict_parser = dict_parser
        self.etree_main = self.dict_parser.get_def_main()

        self.word_frequency = None
        self.def_groups = None
        self.examples = None
        # self.related_terms = None
        self.nearby_words = None
        # self.synonyms = None
        # self.phrases = None

    def build_children(self):
        self.word_frequency = WordFrequencyGroup(self.dict_parser)
        self.word_frequency.build()

        self.def_groups = DefGroups(self.dict_parser)
        self.def_groups.build()

        self.examples = ExamplesGroup(self.dict_parser)
        self.examples.build()

        # self.related_terms = RelatedTermsGroup(self.dict_parser)
        self.nearby_words = NearbyWordsGroup(self.dict_parser)
        self.nearby_words.build()
        # self.synonyms = SynonymsGroup(self.dict_        #
        # self.phrases = PhrasesGroup(self.dict_parser, self.def_groups[0])

    def translate(self):
        children = []
        if self.word_frequency is not None:
            children.append(self.word_frequency.translate())
        if self.def_groups is not None:
            children.append(self.def_groups.translate())
        if self.examples is not None:
            children.append(self.examples.translate())
        """if self.related_terms is not None:
            children.append(self.related_terms.translate())"""
        if self.nearby_words is not None:
            children.append(self.nearby_words.translate())
        """if self.synonyms is not None:
             children.append(self.synonyms.translate())"""
        """if self.phrases is not None:
            children.append(self.phrases.translate())"""

        return {'word': children}


class HtmlToJson:
    def __init__(self, word_name, html_content):
        self.word_name = word_name
        self.html_content = html_content
        self.translated_obj = None

    def translate(self):
        root = etree.HTML(self.html_content)
        dict_parser = DictParser(root, self.word_name)

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
        dict_parser = DictRelatedParser(root)

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
        dict_parser = DictSynParser(root, self.word_name)

        main_def = MainDefGroupSyn(dict_parser)
        main_def.build_children()
        self.translated_obj = main_def.translate()
        return self.translated_obj
