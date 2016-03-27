from .syn_parser import SynParser


class JsonGroup:
    def __init__(self, dict_parser: SynParser):
        self.dict_parser = dict_parser

    def translate(self) -> dict:
        pass


class SynListGroup(JsonGroup):
    def __init__(self, dict_parser: SynParser, etree_elem):
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
    def __init__(self, dict_parser: SynParser, etree_elem):
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
    def __init__(self, dict_parser: SynParser, etree_elem):
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
    def __init__(self, dict_parser: SynParser, etree_def_group):
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
