import re

from src.colors import ColoredText


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
        if "examples" in obj.keys():
            text = ""
            for example in obj["examples"]:
                text += "{}e.g. {}\n".format(DefinitionReader.tab, example)
            return text
        return ""

    @staticmethod
    def _read_def_item(definition: dict, level: int) -> list:
        items = list()

        def_text = ("*) " if level > 0 else "") + DefinitionReader._read_category(definition) + definition["def"] + "\n"

        items.append(def_text)
        items.append(DefinitionReader._read_example(definition))
        if '' in items:
            items.remove('')

        return items

    @staticmethod
    def read_definition(obj: dict):
        return "o) " + "".join(DefinitionReader._read_def_item(obj, level=0))

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
            text += ColoredText.colored_gram(obj["value"])

        return text

    def read_gram_group(self, gram_group: dict):
        text = ""
        value = self._read_gram_value(gram_group)

        if len(value):
            text += value + "\n"

        defs = DefinitionReader(gram_group["defs"])
        text += defs()
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
        return ColoredText.colored_word(obj["word"])

    @staticmethod
    def _read_word_forms(obj: dict):
        text = ""

        if "forms" in obj.keys() and len(obj["forms"]) > 0:
            forms = "(" + ", ".join(obj["forms"]) + ")"

            text += ColoredText.colored_title(forms)

        return text

    @staticmethod
    def _read_note(obj: dict):
        text = ""
        if "note" in obj.keys():
            text = "NOTE: " + obj["note"]

        return text

    def read_def_group(self, def_group: dict):
        text = self._read_word(def_group)
        forms = self._read_word_forms(def_group)
        note = self._read_note(def_group)

        if len(forms):
            text += " " + forms + "\n\n"
        else:
            text += "\n"

        if len(note):
            text += note + "\n\n"

        g_reader = GramGroupReader(def_group["gram_groups"])
        text += g_reader()

        return text

    def __call__(self) -> str:
        text = ""

        for item in self.def_groups:
            text += self.read_def_group(item)

        return text


class JsonLearnReader:
    def __init__(self, content: dict, use_colors: bool = True):
        self.content = content

        if use_colors:
            ColoredText.init_values()

    def definitions(self) -> str:
        text = ColoredText.colored_h1("[cobuild]\n")

        reader = DefGroupReader(self.content)
        text += reader()

        return text

    def read_content(self) -> str:
        text = self.definitions()
        text += "\n"

        return text
