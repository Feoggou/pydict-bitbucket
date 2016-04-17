import re

from . import colors


class DefinitionReader:
    tab = "    "

    def __init__(self, defs: list):
        self.defs = defs

    @staticmethod
    def _read_category(obj: dict):
        if "category" in obj.keys():
            return "({}) ".format(obj["category"])
        return ""

    @staticmethod
    def _read_example(obj: dict):
        if "example" in obj.keys():
            return "{}e.g. {}\n".format(DefinitionReader.tab, obj["example"])
        return ""

    @staticmethod
    def _read_subdefinition(subdef: dict):
        items = DefinitionReader._read_def_item(subdef)
        return "".join([" " * 5 + line for line in items])

    @staticmethod
    def _read_def_subgroup(subgroup: dict):
        text = "o) "
        text += DefinitionReader._read_category(subgroup) + "\n"

        for subdef in subgroup["def_subgroup"]:
            text += DefinitionReader._read_subdefinition(subdef)
        return text

    @staticmethod
    def _read_def_item(definition: dict) -> list:
        items = list()

        items.append(DefinitionReader._read_category(definition) + definition["def"] + "\n")
        items.append(DefinitionReader._read_example(definition))
        if '' in items:
            items.remove('')

        return items

    @staticmethod
    def read_definition(obj: dict):
        if "def_subgroup" in obj.keys():
            return DefinitionReader._read_def_subgroup(obj)
        else:
            return "o) " + "".join(DefinitionReader._read_def_item(obj))

    def __call__(self) -> str:
        text = ""

        for item in self.defs:
            text += self.read_definition(item)

        return text


class GramGroupReader:
    def __init__(self, obj: dict):
        self.gram_groups = obj

    @staticmethod
    def _read_gram_value(obj: dict):
        text = ""

        if "value" in obj.keys():
            text += colors.RED + obj["value"] + colors.RESET + "\n"

        return text

    def read_gram_group(self, gram_group: dict):
        text = ""
        text += self._read_gram_value(gram_group)

        def_reader = DefinitionReader(gram_group["defs"])
        text += def_reader()
        text += "\n"
        return text

    def __call__(self) -> str:
        text = ""

        for item in self.gram_groups:
            text += self.read_gram_group(item)

        return text


class DefGroupReader:
    def __init__(self, obj: dict):
        self.def_groups = obj

    @staticmethod
    def _read_word(obj: dict):
        return colors.BOLDBLACK + obj["word"] + colors.RESET + "\n"

    @staticmethod
    def _read_semantics(def_group):
        if "semantics" not in def_group:
            return ""

        text = colors.BLUE + "\nSEMANTICS\n" + colors.RESET
        text += def_group["semantics"] + "\n\n"

        return text

    def read_def_group(self, def_group: dict):
        text = self._read_word(def_group)

        g_reader = GramGroupReader(def_group["gram_groups"])
        text += g_reader()

        text += self._read_semantics(def_group) + "\n"

        return text

    def get_all_related(self) -> list:
        in_rel_list = []

        for item in self.def_groups:
            if "related" in item.keys():
                in_rel_list += item["related"]

        return in_rel_list

    def __call__(self) -> str:
        text = ""

        for item in self.def_groups:
            text += self.read_def_group(item)

        return text


class SynLineReader:
    def __init__(self, synonyms: list):
        self.synonyms = synonyms

    @staticmethod
    def read_line(item: dict):
        text = "o) "
        # TODO
        if "category" in item.keys():
            text += "({}) ".format(item["category"])

        text += ", ".join(item["line"])
        text += "\n"

        return text

    def __call__(self) -> str:
        text = ""

        for item in self.synonyms:
           text += self.read_line(item)

        return text


class SynGramGroupReader:
    def __init__(self, obj: dict):
        self.gram_groups = obj

    @staticmethod
    def _read_gram_value(obj: dict):
        text = ""

        if "value" in obj.keys():
            text += colors.RED + obj["value"] + "\n" + colors.RESET

        return text

    def read_gram_group(self, gram_group: dict):
        text = ""
        text += self._read_gram_value(gram_group)

        syn_reader = SynLineReader(gram_group["synonyms"])
        text += syn_reader()
        text += "\n"

        return text

    def __call__(self) -> str:
        text = ""

        for item in self.gram_groups:
            text += self.read_gram_group(item["gram_group"])

        return text


class SynGroupReader:
    def __init__(self, obj: dict):
        self.def_groups = obj

    @staticmethod
    def _read_word(obj: dict):
        return colors.BOLDBLACK + obj["word"] + "\n" + colors.RESET

    def read_syn_group(self, def_group: dict):
        text = self._read_word(def_group)

        g_reader = SynGramGroupReader(def_group["gram_groups"])
        text += g_reader()

        return text

    def __call__(self) -> str:
        text = ""

        for item in self.def_groups:
            text += self.read_syn_group(item)

        return text


class JsonReader:
    def __init__(self, content: dict):
        self.content = content
        self.keys = {
            "frequency": self.frequency,
            "def_groups": self.definitions,
            "translations": self.translations,
            "synonyms": self.synonyms,
            "examples": self.examples,
            "my_examples": self.my_examples,
            "nearby_words": self.nearby,
            "related_words": self.related,
        }

    def frequency(self) -> str:
        return  colors.RED + "[{}]\n\n".format(self.content["frequency"]) + colors.RESET

    def definitions(self) -> str:
        text = colors.BLUE + "DEFINTIONS\n" + colors.RESET

        reader = DefGroupReader(self.content["def_groups"])
        text += reader()

        return text

    def synonyms(self):
        text = colors.BLUE + "SYNONYMS\n" + colors.RESET

        reader = SynGroupReader(self.content["synonyms"])
        text += reader()

        text += "\n"

        return text

    def translations(self) -> str:
        text = colors.BLUE + "TRANSLATIONS\n" + colors.RESET

        text += "\n".join([x for x in self.content["translations"]])
        text += "\n\n\n"

        return text

    def examples(self) -> str:
        text = colors.BLUE + "EXAMPLES\n" + colors.RESET
        text += "\n".join("o) " + example["example"] for example in self.content["examples"])

        text += "\n\n"
        return text

    def my_examples(self) -> str:
        text = colors.BLUE + "MY EXAMPLES\n" + colors.RESET
        text += "\n".join("o) " + example["example"] for example in self.content["my_examples"])

        text += "\n\n"
        return text

    def nearby(self) -> str:
        return "\n".join(self.content["nearby_words"])

    def related(self) -> str:
        return "\n".join(self.content["related_words"])

    def read_by_key(self, key: str) -> str:
        if key in self.content and len(self.content[key]):
            return self.keys[key]()
        return ""

    def read_content(self):
        text = self.read_by_key("frequency")
        text += self.read_by_key("def_groups")
        text += self.read_by_key("translations")
        text += self.read_by_key("synonyms")
        text += self.read_by_key("examples")
        text += self.read_by_key("my_examples")
        text += "\n"

        return text

    # NOTE: has no test.
    def read_all_related(self, word: str):
        rel_list = self.read_by_key("related_words").split("\n")
        nby_list = self.read_by_key("nearby_words").split("\n")

        pattern = re.compile(r'\b{}\b'.format(word))
        nby_list = [x for x in nby_list if re.search(pattern, x)]

        def_groups = DefGroupReader(self.content["def_groups"])
        in_rel_list = def_groups.get_all_related()

        all_items = set()
        all_items.update(rel_list)
        all_items.update(in_rel_list)
        all_items.update(nby_list)

        text = "\n".join(all_items)
        text += "\n\n{} related\n{} in def groups\n{} nearby\n{} total".format(
            len(rel_list), len(in_rel_list), len(nby_list), len(all_items))

        return text
