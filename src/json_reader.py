

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
        if "semantics" not in def_group:
            return ""

        text = "\nSEMANTICS\n"
        text += def_group["semantics"] + "\n\n"

        return text

    def read_def_group(self, def_group: dict):
        text = self._read_word(def_group)

        g_reader = GramGroupReader(def_group["gram_groups"])
        text += g_reader()

        text += self._read_semantics(def_group) + "\n"

        return text

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
            text += obj["value"] + "\n"

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
        return obj["word"] + "\n"

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
            "examples": self.examples
        }

    def frequency(self) -> str:
        return "[{}]\n\n".format(self.content["frequency"])

    def definitions(self) -> str:
        text = "DEFINTIONS\n"

        reader = DefGroupReader(self.content["def_groups"])
        text += reader()

        return text

    def synonyms(self):
        text = "SYNONYMS\n"

        reader = SynGroupReader(self.content["synonyms"])
        text += reader()

        text += "\n"

        return text

    def translations(self) -> str:
        text = "TRANSLATIONS\n"

        text += "\n".join([x for x in self.content["translations"]])
        text += "\n\n\n"

        return text

    def examples(self) -> str:
        text = "EXAMPLES\n"
        text += "\n".join("o) " + example["example"] for example in self.content["examples"])

        text += "\n"
        return text

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
        text += "\n"

        return text
