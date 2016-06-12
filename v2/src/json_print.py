from src.json_reader import JsonReader


class JsonPrinter:
    def print(self, content):
        reader = JsonReader(content, use_colors=True)
        text = reader.read_content("do")
        print(text)

