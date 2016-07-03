from src.json_reader import JsonReader
from src.json_learn_reader import JsonLearnReader
from src.json_syn_reader import JsonSynReader


class JsonPrinter:
    def output(self, text):
        print(text)

    def print(self, content):
        reader = JsonReader(content, use_colors=True)
        text = reader.read_content("do")
        self.output(text)

    def print_learn(self, content):
        reader = JsonLearnReader(content, use_colors=True)
        text = reader.read_content()
        self.output(text)

    def print_syn(self, content):
        reader = JsonSynReader(content, use_colors=True)
        text = reader.read_content()
        self.output(text)
