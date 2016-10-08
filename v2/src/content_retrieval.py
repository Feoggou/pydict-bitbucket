from src import html_fetcher
from src.html_parser import HtmlParser


class ContentRetrieval:
    @staticmethod
    def fetch(word: str, what: str):
        fetcher = html_fetcher.HtmlFetcher(word)
        return fetcher.fetch(what)

    def get_def_content(self, word: str):
        html_content = self.fetch(word, "def")
        # TODO: save html

        parser = HtmlParser()
        def_content = parser.parse(word, html_content)
        learn_content = parser.parse_learn(word, html_content)

        return def_content, learn_content

    def get_syn_content(self, word: str):
        html_content = self.fetch(word, "syn")
        # TODO: save html

        parser = HtmlParser()
        return parser.parse_syn(word, html_content)
