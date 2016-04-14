

class DefinitionReader:
    tab = "    "

    def __init__(self, defs: list):
        self.defs = defs

    @staticmethod
    def _read_def_subgroup(subgroup: dict, indent: int = 0):
        text = ""
        if "category" in subgroup.keys():
            text += "({}) ".format(subgroup["category"])

        text = "{}o) {}\n".format(DefinitionReader.tab * indent, text)
        for subdef in subgroup["def_subgroup"]:
            text += DefinitionReader._read_def_item(subdef, indent + 1)
        return text

    @staticmethod
    def _read_def_item(definition: dict, indent: int = 0):
        text = definition["def"]
        if "example" in definition.keys():
            text += "\n{}e.g. {}".format(DefinitionReader.tab * (indent + 1), definition["example"])
        if "category" in definition.keys():
            text = "({}) {}".format(definition["category"], text)

        text = (DefinitionReader.tab * indent) + ("o) " if indent == 0 else " ") + text
        text += "\n"
        return text

    @staticmethod
    def read_definition(obj: dict):
        if "def_subgroup" in obj.keys():
            return DefinitionReader._read_def_subgroup(obj)
        else:
            return DefinitionReader._read_def_item(obj)

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
            text += obj["value"] + "\n"

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
        return obj["word"] + "\n"

    @staticmethod
    def _read_semantics(def_group):
        text = "\nSEMANTICS\n"
        text += def_group["semantics"] + "\n"

        return text

    def read_def_group(self, def_group: dict):
        text = self._read_word(def_group)

        g_reader = GramGroupReader(def_group["gram_groups"])
        text += g_reader()

        text += self._read_semantics(def_group)

        return text

    def __call__(self) -> str:
        text = ""

        for item in self.def_groups:
            text += self.read_def_group(item)

        return text


class JsonReader:
    def __init__(self, content: dict):
        self.content = content
        self.keys = {
            "frequency": self.frequency,
            "def_groups": self.definitions,
        }

    def frequency(self) -> str:
        return "[{}]\n\n".format(self.content["frequency"])

    def definitions(self) -> str:
        text = "DEFINTIONS\n"

        reader = DefGroupReader(self.content["def_groups"])
        text += reader()

        text += "\n"

        return text

    def read_by_key(self, key: str) -> str:
        if key in self.content and len(self.content[key]):
            return self.keys[key]()
        return ""