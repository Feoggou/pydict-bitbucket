import re

from src.colors import ColoredText


class SynReader:
    tab = "    "

    def __init__(self, syn_line: dict):
        self.syn_line = syn_line

    @staticmethod
    def _read_example(obj: dict):
        if "example" in obj.keys():
            return "{}e.g. {}\n".format(SynReader.tab, obj["example"])
        return ""

    @staticmethod
    def _read_syn_line(obj: dict):
        items = []
        for key in obj.keys():
            if len(obj[key]):
                item = "({}) {}".format(obj[key], key)
            else:
                item = key

            items.append(item)

        text = ", ".join(items)
        return text

    @staticmethod
    def _read_syn_item(syn_obj: dict) -> list:
        items = list()

        def_text = SynReader._read_syn_line(syn_obj["syn_line"]) + "\n"

        items.append(def_text)
        items.append(SynReader._read_example(syn_obj))
        if '' in items:
            items.remove('')

        return items

    @staticmethod
    def read_syn(obj: dict):
        return "o) " + "".join(SynReader._read_syn_item(obj))

    def __call__(self) -> str:
        text = self.read_syn(self.syn_line)

        return text


class DefSynsReader:
    def __init__(self, obj: dict):
        self.syns_groups = obj

    def read_syn_group(self, syn_line: dict):
        text = ""

        def_reader = SynReader(syn_line)
        text += def_reader()
        text += "\n"
        return text

    def __call__(self) -> str:
        text = ""

        for syn_line in self.syns_groups:
            text += self.read_syn_group(syn_line)

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
        value = self._read_gram_value(gram_group)

        text = value + "\n"

        syns_groups = DefSynsReader(gram_group["syns"])
        text += syns_groups()
        text += "\n"
        return text

    def __call__(self) -> str:
        text = ""

        for item in self.gram_groups:
            text += self.read_gram_group(item)

        return text


class DefGroupReader:
    def __init__(self, obj: dict):
        self.def_group = obj

    @staticmethod
    def _read_word(obj: dict):
        return ColoredText.colored_word(obj["word"]) + "\n"

    def read_def_group(self, def_group: dict):
        text = self._read_word(def_group)

        g_reader = GramGroupReader(def_group["gram_groups"])
        text += g_reader()

        return text

    def __call__(self) -> str:
        text = self.read_def_group(self.def_group)

        return text


class JsonSynReader:
    def __init__(self, content: dict, use_colors: bool = True):
        self.content = content

        if use_colors:
            ColoredText.init_values()

    def read_content(self) -> str:
        reader = DefGroupReader(self.content)
        text = reader()
        text += "\n"

        return text
