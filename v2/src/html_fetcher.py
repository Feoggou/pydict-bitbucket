import http
from http import client
import os

from src import config


class WordNotFoundError(RuntimeError):
    def __init__(self, word_name):
        self.value = word_name

    def __str__(self):
        return repr(self.value)


class HtmlFetcher:
    def __init__(self, word: str):
        self.word = word
        self.html_path = config.HTML_SOURCE_PATH

    def fetch(self, what: str):
        """what: either "def" or "str" """

        if what == "def":
            suffix = "_defs.html"
        elif what == "syn":
            suffix = "_syn.html"
        else:
            raise ValueError()

        with open(os.path.join(self.html_path, self.word + suffix), "r") as f:
            return f.read()
