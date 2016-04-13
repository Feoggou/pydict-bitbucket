

class DefGroupReader:
    def __init__(self, obj: dict):
        self.def_groups = obj

    def read_def_group(self, def_group: dict):
        raise NotImplementedError()

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
            "def_groups": self.definitions
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