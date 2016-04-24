from lxml import etree
from .rel_parser import RelatedParser


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

