import re
import os
from collections import OrderedDict

from src import config
from src.colors import ColoredText
from src.json_collector import JsonCollector
from src.json_load import JsonLoader


class SearchResult:
    def __init__(self):
        self.file_names = []
        self.word_forms = []

        ColoredText.init_values()

    def __str__(self):
        text = "\n"

        if len(self.file_names):
            text += "=== FILES ===\n"
            text += "; ".join(self.file_names)

        text += "\n"

        return text


class Search:
    def search(self, expr: str):
        result = SearchResult()

        result.file_names = self.find_files(expr)
        result.word_forms = self.find_word_forms(expr)

        return result

    def find_files(self, expr: str):
        file_names = self.collect_filenames()

        return [x for x in file_names if self.name_matches(x, expr)]

    @staticmethod
    def collect_filenames():
        file_names = [file_name for file_name in os.listdir(config.JSON_DIR_PATH) if
                      os.path.isfile(os.path.join(config.JSON_DIR_PATH, file_name)) and
                      (file_name.endswith(".def") or
                       file_name.endswith(".learn") or
                       file_name.endswith(".syn"))]

        return sorted(file_names)

    @staticmethod
    def name_matches(name: str, what: str) -> bool:
        pattern = re.compile(r'\b{}\b'.format(what))
        return re.search(pattern, name)

    @staticmethod
    def find_word_forms(expr: str):
        collector = JsonCollector()

        results = OrderedDict()

        for file_name in Search.collect_filenames():
            content = JsonLoader().load(file_name)
            file_kind = file_name.split('.')[1]

            forms = collector.collect_word_forms(file_kind, content)
            forms = [x for x in forms if Search.name_matches(x, expr)]

            results[file_name] = forms

        return results
