from .learn_parser import LearnParser


class LearnJsonGroup:
    def __init__(self, dict_parser: LearnParser):
        self.dict_parser = dict_parser

    def translate(self) -> dict:
        pass


# {"category":"slang", "def":"excrement; feces", "example":"dog do", "know": False}
class LearnWordDefinition(LearnJsonGroup):
    def __init__(self, dict_parser: LearnParser, etree_elem):
        LearnJsonGroup.__init__(self, dict_parser)
        self.etree_elem = etree_elem
        self.category = ""
        self.definition = ""
        self.examples = []

    def build(self):
        self.definition = self.dict_parser.get_sense_def(self.etree_elem)
        self.examples = self.dict_parser.get_sense_example(self.etree_elem)
        self.category = self.dict_parser.get_sense_categ(self.etree_elem)

        # if self.definition is None:
        #     self.definition = "(i) " + self.dict_parser.get_sense_def_label(self.etree_elem)

    def translate(self) -> dict:
        json_children = {"def": self.definition, "mark": "good"}

        if len(self.category):
            json_children["category"] = self.category
        if len(self.examples):
            json_children["examples"] = self.examples

        return json_children


class LearnWordForms(LearnJsonGroup):
    def __init__(self, dict_parser: LearnParser, def_group):
        LearnJsonGroup.__init__(self, dict_parser)
        self.forms = []
        self.def_group = def_group

    def build(self):
        self.forms = self.dict_parser.get_word_forms(self.def_group)

    def translate(self) -> dict:
        return self.forms


class LearnGramGroup(LearnJsonGroup):
    def __init__(self, dict_parser: LearnParser, etree_elem):
        LearnJsonGroup.__init__(self, dict_parser)
        self.etree_elem = etree_elem
        self.grammar_value = None
        self.definition = None

    def build(self):
        self.grammar_value = self.dict_parser.get_gram_value(self.etree_elem)
        # if len(self.grammar_value) == 0:
        #     self.grammar_value = None

        senses = self.dict_parser.get_all_sense_items(self.etree_elem)
        assert len(senses) == 1

        definition = LearnWordDefinition(self.dict_parser, senses[0])
        definition.build()
        self.definition = definition.translate()


class LearnDefGroup(LearnJsonGroup):
    def __init__(self, dict_parser: LearnParser, etree):
        LearnJsonGroup.__init__(self, dict_parser)
        self.etree_elem = etree
        self.name = ''
        self.gram_groups = dict()
        self.word_forms = None
        self.note = None

        self.word = dict_parser.get_def_group_text(etree)

    def build(self):
        self.word_forms = LearnWordForms(self.dict_parser, self.etree_elem)
        self.word_forms.build()

        self.note = self.dict_parser.get_note(self.etree_elem)

        gram_groups = self.dict_parser.get_all_grammar_groups(self.etree_elem)
        for etree_item in gram_groups:
            child = LearnGramGroup(self.dict_parser, etree_item)
            child.build()

            if child.definition["def"] is not None:
                if child.grammar_value in self.gram_groups.keys():
                    self.gram_groups[child.grammar_value].append(child.definition)
                else:
                    self.gram_groups[child.grammar_value] = [child.definition]

    def translate(self) -> dict:
        gram_groups = []
        for child in self.gram_groups.keys():
            # assert len(child)

            ggroup_json = dict()
            ggroup_json["defs"] = self.gram_groups[child]
            ggroup_json["value"] = child

            # json_child = child.translate()
            # if json_child is not None:
            #     gram_groups.append(json_child)
            gram_groups.append(ggroup_json)

        gram_groups.sort(key=lambda ggroup : ggroup["value"])

        json_obj = dict()
        json_obj["word"] = self.word
        json_obj["gram_groups"] = gram_groups

        if self.word_forms is not None:
            json_obj["forms"] = self.word_forms.translate()
        if self.note is not None:
            json_obj["note"] = self.note

        return json_obj


class LearnDefGroups(LearnJsonGroup):
    def __init__(self, dict_parser):
        LearnJsonGroup.__init__(self, dict_parser)
        self.children = []

    def build(self):
        etree_groups = self.dict_parser.get_all_def_groups()
        for etree_item in etree_groups:
            child = LearnDefGroup(self.dict_parser, etree_item)
            child.build()
            self.children.append(child)

    def translate(self):
        json_children = []
        for child in self.children:
            json_child = child.translate()
            if json_child is not None:
                json_children.append(json_child)

        return json_children



