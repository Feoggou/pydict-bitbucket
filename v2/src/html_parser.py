from lxml import etree

from src.def_groups import MainDefGroup
from .def_parser import DefParser


class HtmlParser:
    def __init__(self):
        # self.word_name = word_name
        # self.html_content = html_content
        self.translated_obj = None

    def parse(self, word_name, html_content: str):
        root = etree.HTML(html_content)
        dict_parser = DefParser(root, word_name)

        main_def = MainDefGroup(dict_parser)
        main_def.build_children()
        self.translated_obj = main_def.translate()
        return self.translated_obj
