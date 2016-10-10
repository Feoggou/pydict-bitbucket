import os

from src import html_fetcher
from src.html_parser import HtmlParser
from src import config
from src.json_load import JsonLoader


class ContentRetrieval:
    @staticmethod
    def read_json_file(file_name: str):
        return JsonLoader().load(file_name)

    @staticmethod
    def have_word(word: str):
        file_path = os.path.join(config.JSON_DIR_PATH, word + ".def")
        return os.path.exists(file_path)

    @staticmethod
    def fetch(word: str, what: str):
        fetcher = html_fetcher.HtmlFetcher(word)
        return fetcher.fetch(what)

    def get_def_content(self, word: str):
        if not self.have_word(word):
            html_content = self.fetch(word, "def")

            parser = HtmlParser()
            def_content = parser.parse(word, html_content)
            learn_content = parser.parse_learn(word, html_content)

            return def_content, learn_content, False

        return self.read_json_file(word + ".def"),\
               self.read_json_file(word + ".learn"),\
               True

    def get_syn_content(self, word: str):
        html_content = self.fetch(word, "syn")

        parser = HtmlParser()
        return parser.parse_syn(word, html_content)
