from .syn_parser import SynParser

# TODO: try to merge syn_groups with def_groups


class JsonGroup:
    def __init__(self, dict_parser: SynParser):
        self.dict_parser = dict_parser

    def translate(self) -> dict:
        pass


class SynLine(JsonGroup):
    def __init__(self, dict_parser: SynParser, etree_elem):
        JsonGroup.__init__(self, dict_parser)
        self.etree_elem = etree_elem
        self.syns = []
        self.example = ""

    def build(self):
        self.syns = self.dict_parser.get_syn_line(self.etree_elem)
        self.example = self.dict_parser.get_syn_example(self.etree_elem)

    def translate(self) -> dict:
        json_children = {"syn_line": self.syns, "mark": "good"}

        if len(self.example):
            json_children["example"] = self.example

        return json_children


class SynGramGroup(JsonGroup):
    def __init__(self, dict_parser: SynParser, etree_elem):
        JsonGroup.__init__(self, dict_parser)
        self.etree_elem = etree_elem
        self.grammar_value = None
        self.syn_list = None

    def build(self):
        self.grammar_value = self.dict_parser.get_gram_value(self.etree_elem)
        if len(self.grammar_value) == 0:
            self.grammar_value = None

        self.syn_list = []

        senses = self.dict_parser.get_all_sense_items(self.etree_elem)
        for item in senses:
            word = SynLine(self.dict_parser, item)
            word.build()
            self.syn_list.append(word.translate())

    def translate(self) -> dict:
        json_object = {}
        if self.grammar_value is not None:
            json_object["value"] = self.grammar_value
        if self.syn_list is not None:
            json_object["syns"] = self.syn_list

        return json_object


class SynDefGroup(JsonGroup):
    def __init__(self, dict_parser: SynParser):
        JsonGroup.__init__(self, dict_parser)
        self.name = ''
        self.gram_groups = []

        self.word = dict_parser.get_def_group_text()

    def build(self):
        gram_groups = self.dict_parser.get_all_grammar_groups()
        for etree_item in gram_groups:
            child = SynGramGroup(self.dict_parser, etree_item)
            child.build()
            self.gram_groups.append(child)

    def translate(self) -> dict:
        gram_groups = []
        for child in self.gram_groups:
            json_child = child.translate()
            if json_child is not None:
                gram_groups.append(json_child)

        json_obj = {"word": self.word, "gram_groups": gram_groups}

        return json_obj
