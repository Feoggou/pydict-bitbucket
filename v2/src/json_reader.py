import re

from src import colors


class ColoredText:
    reset_color = ""
    title_color = ""
    h1_color = ""
    word_color = ""
    gram_color = ""
    usage_color = ""

    @staticmethod
    def init_values():
        ColoredText.reset_color = colors.RESET
        ColoredText.title_color = colors.RED
        ColoredText.h1_color = colors.BLUE
        ColoredText.word_color = colors.BOLDBLACK
        ColoredText.gram_color = colors.RED
        ColoredText.usage_color = colors.GREEN

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

    @staticmethod
    def colored_usage(s: str):
        return ColoredText.usage_color + s + ColoredText.reset_color


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
    def _read_subdefinition(subdef: dict, level: int):
        items = DefinitionReader._read_def_item(subdef, level)
        return "".join([" " * (level * 5) + line for line in items])

    @staticmethod
    def _read_def_subgroup(subgroup: dict, level: int):
        text = "o) "
        text += DefinitionReader._read_category(subgroup) + "\n"

        for subdef in subgroup["def_subgroup"]:
            text += DefinitionReader._read_subdefinition(subdef, level)
        return text

    @staticmethod
    def _read_def_item(definition: dict, level: int) -> list:
        items = list()

        def_text = ""

        if "def" in definition.keys():
            def_text = ("*) " if level > 0 else "") + DefinitionReader._read_category(definition) + definition["def"] + "\n"
        elif "def_subgroup" in definition.keys():
            # sub-subdefinition - beam
            def_text = DefinitionReader._read_def_subgroup(definition, level + 1)

        items.append(def_text)

        items.append(DefinitionReader._read_example(definition))
        if '' in items:
            items.remove('')

        return items

    @staticmethod
    def read_definition(obj: dict):
        if "def_subgroup" in obj.keys():
            return DefinitionReader._read_def_subgroup(obj, level=1)
        else:
            return "o) " + "".join(DefinitionReader._read_def_item(obj, level=0))

    def __call__(self) -> str:
        text = ""

        for item in self.defs:
            text += self.read_definition(item)

        return text


class DefUsageGroupReader:
    def __init__(self, obj: dict):
        self.usage_groups = obj

    def read_usage_group(self, usage_name: str):
        text = ""

        if len(usage_name) > 0:
            text += ColoredText.colored_usage(usage_name + ":\n")

        def_reader = DefinitionReader(self.usage_groups[usage_name])
        text += def_reader()
        text += "\n"
        return text

    def __call__(self) -> str:
        text = ""

        for usage_name in self.usage_groups:
            text += self.read_usage_group(usage_name)

        return text


class GramGroupReader:
    def __init__(self, obj: dict):
        self.gram_groups = obj

    @staticmethod
    def _read_gram_value(obj: dict):
        text = ""

        if "value" in obj.keys():
            text += ColoredText.colored_gram(obj["value"])

        return text

    @staticmethod
    def _read_word_forms(obj: dict):
        text = ""

        if "forms" in obj.keys() and len(obj["forms"]["items"]) > 0:
            forms = "(" + ", ".join(obj["forms"]["items"]) + ")"
            if "info" in obj["forms"].keys():
                info = obj["forms"]["info"]
                if len(info) > 0:
                    forms += " -- " + info

            text += ColoredText.colored_title(forms)

        return text

    def read_gram_group(self, gram_group: dict):
        text = ""
        value = self._read_gram_value(gram_group)
        forms = self._read_word_forms(gram_group)

        if len(value) and len(forms):
            text += value + " " + forms + "\n"
        elif len(value) == len(forms) == 0:
            pass
        else:
            text += value + forms + "\n"

        usage_groups = DefUsageGroupReader(gram_group["defs"])
        text += usage_groups()
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
    def _read_frequency(obj: dict) -> str:
        if "frequency" in obj and len(obj["frequency"]) > 0:
            return ColoredText.colored_title("[{}]\n\n".format(obj["frequency"])) + "\n"

        return ""

    def read_def_group(self, def_group: dict):
        text = self._read_word(def_group)

        text += self._read_frequency(def_group)

        g_reader = GramGroupReader(def_group["gram_groups"])
        text += g_reader()

        return text

    def __call__(self) -> str:
        text = ""

        for item in self.def_groups:
            text += self.read_def_group(item)

        return text


class JsonReader:
    def __init__(self, content: dict, use_colors: bool = True):
        self.content = content
        self.keys = {
            # "frequency": self.frequency,
            "def_groups": self.definitions,
            "translations": self.translations,
            "examples": self.examples,
            # "my_examples": self.my_examples,
        }

        if use_colors:
            ColoredText.init_values()

    """def frequency(self) -> str:
        return ColoredText.colored_title("[{}]\n\n".format(self.content["frequency"]))"""

    def definitions(self) -> str:
        text = ColoredText.colored_h1("DEFINTIONS\n")

        reader = DefGroupReader(self.content["def_groups"])
        text += reader()

        return text

    def translations(self) -> str:
        text = ColoredText.colored_h1("TRANSLATIONS\n")

        for transl in self.content["translations"]:
            text += ColoredText.colored_word(transl["word"]) + "\n"
            text += ColoredText.colored_gram(transl["value"]) + "\n"
            text += transl["def"] + "\n"
            text += "{}e.g. {}\n".format(DefinitionReader.tab, transl["example"])

        text += "\n\n\n"

        return text

    def examples(self) -> str:
        text = ColoredText.colored_h1("EXAMPLES\n")
        text += "\n".join("o) " + example for example in self.content["examples"])

        text += "\n\n"
        return text

    """def my_examples(self) -> str:
        text = ColoredText.colored_h1("MY EXAMPLES\n")
        text += "\n".join("o) " + example["example"] for example in self.content["my_examples"])

        text += "\n\n"
        return text"""

    def read_by_key(self, key: str) -> str:
        if key in self.content and len(self.content[key]):
            return self.keys[key]()
        return ""

    def read_content(self, word) -> str:
        # text = self.read_by_key("frequency")
        text = self.read_by_key("def_groups")
        text += self.read_by_key("translations")
        text += self.read_by_key("examples")
        # text += self.read_by_key("my_examples")
        text += "\n"

        return text
