

class JsonReader:
    def __init__(self, content: dict):
        self.content = content
        self.keys = {
            "frequency": self.frequency,
            "def_groups": self.definitions
        }

    def frequency(self) -> str:
        # # TODO: could be nicer with a dictionary { key : function }
        # if len(self.content["frequency"]) == 0:
        #     return ""
        return "[{}]\n\n".format(self.content["frequency"])

    def _read_gram_groups(self, obj: dict):
        raise NotImplementedError()

    def definitions(self) -> str:
        text = "DEFINTIONS\n"
        for gram_groups in self.content["def_groups"]:
            text += self._read_gram_groups(gram_groups)
            pass

        text += "\n"

        return text

    def read_by_key(self, key: str) -> str:
        if key in self.content and len(self.content[key]):
            return self.keys[key]()
        return ""