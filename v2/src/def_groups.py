from .def_parser import DefParser


class JsonGroup:
    def __init__(self, dict_parser: DefParser):
        self.dict_parser = dict_parser

    def translate(self) -> dict:
        pass


class WordFrequencyGroup(JsonGroup):
    def __init__(self, dict_parser: DefParser, def_group):
        JsonGroup.__init__(self, dict_parser)
        self.word_freq = ''
        self.def_group = def_group

    def build(self):
        self.word_freq = self.dict_parser.get_word_freq(self.def_group)

    def translate(self) -> dict:
        return self.word_freq


class ExamplesGroup(JsonGroup):
    def __init__(self, dict_parser):
        JsonGroup.__init__(self, dict_parser)
        self.examples = {}

    def build(self):
        examples = self.dict_parser.get_all_examples()
        self.examples = examples

    def translate(self):
        return self.examples


class DefSubgroup(JsonGroup):
    def __init__(self, dict_parser: DefParser, etree_elem):
        JsonGroup.__init__(self, dict_parser)
        self.subdefs = []
        self.etree_elem = etree_elem

    def build(self):
        senses = self.dict_parser.get_all_sense_items(self.etree_elem)

        for elem in senses:
            word = WordDefinition(self.dict_parser, elem, usage_is_categ=True)
            word.build()
            self.subdefs.append(word.translate())

    def translate(self) -> dict:
        return self.subdefs


# {"category":"slang", "def":"excrement; feces", "example":"dog do", "know": False}
class WordDefinition(JsonGroup):
    def __init__(self, dict_parser: DefParser, etree_elem, usage_is_categ: bool=False):
        JsonGroup.__init__(self, dict_parser)
        self.etree_elem = etree_elem
        self.category = ""
        self.definition = ""
        self.example = ""
        self.subgroup = None
        self.usage = ""
        self.usage_is_categ = usage_is_categ

    def get_usage(self):
        return self.usage

    def build(self):
        self.definition = self.dict_parser.get_sense_def(self.etree_elem)
        self.example = self.dict_parser.get_sense_example(self.etree_elem)
        self.category = self.dict_parser.get_sense_categ(self.etree_elem)
        self.usage = self.dict_parser.get_sense_usage(self.etree_elem)

        if self.usage_is_categ:
            self.category += self.usage

        if len(self.dict_parser.get_all_sense_items(self.etree_elem)):
            self.subgroup = DefSubgroup(self.dict_parser, self.etree_elem)
            self.subgroup.build()
        else:
            if self.definition is None:
                self.definition = "(i) " + self.dict_parser.get_sense_def_label(self.etree_elem)

    def translate(self) -> dict:
        if self.subgroup is not None:
            # assert self.subgroup is not None
            json_children = {"def_subgroup": self.subgroup.translate()}
        else:
            json_children = {"def": self.definition, "mark": "good"}

        if len(self.category):
            json_children["category"] = self.category
        if len(self.example):
            json_children["example"] = self.example

        return json_children


class UsageGroups(JsonGroup):
    def __init__(self, dict_parser: DefParser, sense_elems):
        JsonGroup.__init__(self, dict_parser)
        self.etree_elems = sense_elems
        self.usages = {}

    def build(self):
        self.usages = {}
        for elem in self.etree_elems:
            usage = self.dict_parser.get_sense_usage(elem)
            # print("usage: ", usage)
            if usage not in self.usages:
                self.usages[usage] = []

            word = WordDefinition(self.dict_parser, elem)
            word.build()
            self.usages[usage].append(word.translate())

    def names(self):
        return set(self.usages.keys())

    def translate(self) -> dict:
        # print("\n\nusages: ", self.usages)
        return self.usages


class WordForms(JsonGroup):
    def __init__(self, dict_parser: DefParser, def_group):
        JsonGroup.__init__(self, dict_parser)
        self.forms = []
        self.info = ''
        self.def_group = def_group

    def build(self):
        self.forms = self.dict_parser.get_word_forms(self.def_group)
        self.info = self.dict_parser.get_word_forms_info(self.def_group)

    def translate(self) -> dict:
        return {"items": self.forms, "info": self.info}


# {"gram_group": [{"word_forms": "did, done, doing"}, {"grammar_value": "transitive verb"}, {"defs": []}]}
class GramGroup(JsonGroup):
    def __init__(self, dict_parser: DefParser, etree_elem):
        JsonGroup.__init__(self, dict_parser)
        self.etree_elem = etree_elem
        self.word_forms = None
        self.grammar_value = None
        self.defs = None

    def build(self):
        self.word_forms = WordForms(self.dict_parser, self.etree_elem)
        self.word_forms.build()

        self.grammar_value = self.dict_parser.get_gram_value(self.etree_elem)
        if len(self.grammar_value) == 0:
            self.grammar_value = None

        senses = self.dict_parser.get_all_sense_items(self.etree_elem)
        self.defs = UsageGroups(self.dict_parser, senses)
        self.defs.build()

    def translate(self) -> dict:
        json_object = {}
        if self.word_forms is not None:
            json_object["forms"] = self.word_forms.translate()
        if self.grammar_value is not None:
            json_object["value"] = self.grammar_value
        if self.defs is not None:
            json_object["defs"] = self.defs.translate()

        return json_object


class DefGroup(JsonGroup):
    def __init__(self, dict_parser: DefParser, etree):
        JsonGroup.__init__(self, dict_parser)
        self.etree_elem = etree
        self.name = ''
        # self.semantics = None --- HAVE NO SEMANTICS, AFAIK
        self.gram_groups = []
        self.frequency = None
        self.derived_forms = None

        self.origin = None
        self.note = None
        self.word = dict_parser.get_def_group_text(etree)

    def build(self):
        self.note = self.dict_parser.get_note(self.etree_elem)

        gram_groups = self.dict_parser.get_all_grammar_groups(self.etree_elem)
        for etree_item in gram_groups:
            child = GramGroup(self.dict_parser, etree_item)
            child.build()
            self.gram_groups.append(child)

        self.origin = self.dict_parser.get_etymology(self.etree_elem)
        if len(self.origin) == 0:
            self.origin = None

        derived_form, gram_value = self.dict_parser.get_derived_forms(self.etree_elem)
        if len(derived_form):
            self.derived_forms = {derived_form: gram_value}
        self.frequency = WordFrequencyGroup(self.dict_parser, self.etree_elem)
        self.frequency.build()

    def translate(self) -> dict:
        gram_groups = []
        for child in self.gram_groups:
            json_child = child.translate()
            if json_child is not None:
                gram_groups.append(json_child)

        json_obj = {"word": self.word, "gram_groups": gram_groups}

        if self.frequency is not None:
            json_obj["frequency"] = self.frequency.translate()

        if self.origin is not None:
            json_obj["origin"] = self.origin

        if self.derived_forms is not None:
            json_obj["derived_forms"] = self.derived_forms

        if self.note is not None:
            json_obj["note"] = self.note

        return json_obj


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
        pass

    def translate(self):
        json_children = []
        for child in self.children:
            json_child = child.translate()
            if json_child is not None:
                json_children.append(json_child)

        return json_children


class MainDefGroup:
    def __init__(self, dict_parser: DefParser):
        self.dict_parser = dict_parser
        self.def_groups = None
        self.examples = None
        self.translations = None

    def build_children(self):
        self.def_groups = DefGroups(self.dict_parser)
        self.def_groups.build()

        self.examples = ExamplesGroup(self.dict_parser)
        self.examples.build()

        self.translations = self.dict_parser.get_all_translations()

    def translate(self):
        json_object = {}
        if self.def_groups is not None:
            json_object["def_groups"] = self.def_groups.translate()
        if self.examples is not None:
            json_object["examples"] = self.examples.translate()
        if self.translations is not None:
            json_object["translations"] = self.translations

        return json_object


