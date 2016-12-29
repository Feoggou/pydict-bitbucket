from lxml import etree

from .learn_groups import LearnDefGroups
from .def_groups import MainDefGroup
from .syn_groups import SynDefGroup

from .def_parser import DefParser
from .learn_parser import LearnParser
from .syn_parser import SynParser


class HtmlParser:
    def __init__(self):
        self.translated_obj = None

    def parse(self, word_name, html_content: str):
        root = etree.HTML(html_content)
        dict_parser = DefParser(root, word_name)

        main_def = MainDefGroup(dict_parser)
        main_def.build_children()
        self.translated_obj = main_def.translate()
        return self.translated_obj

    def parse_syn(self, word_name, html_content: str):
        root = etree.HTML(html_content)
        dict_parser = SynParser(root, word_name)

        main_def = SynDefGroup(dict_parser)
        main_def.build()
        self.translated_obj = main_def.translate()
        return self.translated_obj

    def parse_learn(self, word_name, html_content: str):
        root = etree.HTML(html_content)
        dict_parser = LearnParser(root, word_name)

        self.def_groups = LearnDefGroups(dict_parser)
        self.def_groups.build()
        return self.def_groups.translate()

