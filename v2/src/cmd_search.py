import re
import os

from src import config
from src.colors import ColoredText


class SearchResult:
    def __init__(self):
        self.file_names = []
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
        return result

    def find_files(self, expr: str):
        file_names = self.collect_filenames()

        return [x for x in file_names if self.file_name_matches(x, expr)]

    @staticmethod
    def collect_filenames():
        file_names = [file_name for file_name in os.listdir(config.JSON_DIR_PATH) if
                      os.path.isfile(os.path.join(config.JSON_DIR_PATH, file_name)) and
                      (file_name.endswith(".def") or
                       file_name.endswith(".learn") or
                       file_name.endswith(".syn"))]

        return sorted(file_names)

    @staticmethod
    def file_name_matches(file_name: str, what: str) -> bool:
        pattern = re.compile(r'\b{}\b'.format(what))
        return re.search(pattern, file_name)
