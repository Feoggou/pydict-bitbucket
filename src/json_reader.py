import re

from . import colors


class ColoredText:
    reset_color = ""
    title_color = ""
    h1_color = ""
    word_color = ""
    gram_color = ""

    @staticmethod
    def init_values():
        ColoredText.reset_color = colors.RESET
        ColoredText.title_color = colors.RED
        ColoredText.h1_color = colors.BLUE
        ColoredText.word_color = colors.BOLDBLACK
        ColoredText.gram_color = colors.RED

    @staticmethod
    def colored_title(s: str):
        return ColoredText.title_color + s + ColoredText.reset_color

    @staticmethod
    def colored_h1(s: str):
        return ColoredText.h1_color + s + ColoredText.reset_color

    @staticmethod
    def colored_word(s: str):
        return ColoredText.word_color + s + ColoredText.reset_color

    @staticmethod
    def colored_gram(s: str):
        return ColoredText.gram_color + s + ColoredText.reset_color


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
            text += ColoredText.colored_gram(obj["value"]) + "\n"

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
        return ColoredText.colored_word(obj["word"]) + "\n"

    @staticmethod
    def _read_semantics(def_group):
        if "semantics" not in def_group:
            return ""

        text = ColoredText.colored_h1("\nSEMANTICS\n")
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
            text += ColoredText.colored_gram(obj["value"] + "\n")

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
        return ColoredText.colored_word(obj["word"] + "\n")

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
    def __init__(self, content: dict, use_colors: bool = True):
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

        if use_colors:
            ColoredText.init_values()

    def frequency(self) -> str:
        return ColoredText.colored_title("[{}]\n\n".format(self.content["frequency"]))

    def definitions(self) -> str:
        text = ColoredText.colored_h1("DEFINTIONS\n")

        reader = DefGroupReader(self.content["def_groups"])
        text += reader()

        return text

    def synonyms(self):
        text = ColoredText.colored_h1("SYNONYMS\n")

        reader = SynGroupReader(self.content["synonyms"])
        text += reader()

        text += "\n"

        return text

    def translations(self) -> str:
        text = ColoredText.colored_h1("TRANSLATIONS\n")

        text += "\n".join([x for x in self.content["translations"]])
        text += "\n\n\n"

        return text

    def examples(self) -> str:
        text = ColoredText.colored_h1("EXAMPLES\n")
        text += "\n".join("o) " + example["example"] for example in self.content["examples"])

        text += "\n\n"
        return text

    def my_examples(self) -> str:
        text = ColoredText.colored_h1("MY EXAMPLES\n")
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

    def read_content(self, word) -> str:
        text = self.read_by_key("frequency")
        text += self.read_by_key("def_groups")
        text += self.read_by_key("translations")
        text += self.read_by_key("synonyms")
        text += self.read_by_key("examples")
        text += self.read_all_related(word, simple=True)
        text += self.read_by_key("my_examples")
        text += "\n"

        return text

    # NOTE: has no test.
    def read_all_related(self, word: str, simple: bool = False):
        all_items, in_rel_list, nby_list, rel_list = self.get_all_related(word)

        if simple:
            text = ""
            if len(all_items):
                text = ColoredText.colored_h1("RELATED\n") + ", ".join(sorted(all_items))
        else:
            text = "\n".join(all_items)
            text += "\n\n{} related\n{} in def groups\n{} nearby\n{} total".format(
                len(rel_list), len(in_rel_list), len(nby_list), len(all_items))

        return text

    def get_all_related(self, word):
        rel_list = self.read_by_key("related_words").split("\n")
        nby_list = self.read_by_key("nearby_words").split("\n")

        pattern = re.compile(r'\b{}\b'.format(word))
        nby_list = [x for x in nby_list if re.search(pattern, x)]

        def_groups = DefGroupReader(self.content["def_groups"])
        in_rel_list = def_groups.get_all_related()

        if "" in rel_list:
            rel_list.remove("")
        if "" in nby_list:
            nby_list.remove("")
        if "" in in_rel_list:
            in_rel_list.remove("")

        all_items = set()
        all_items.update(rel_list)
        all_items.update(in_rel_list)
        all_items.update(nby_list)

        return all_items, in_rel_list, nby_list, rel_list
