from src import html_fetcher
from src.html_parser import HtmlParser


class ContentRetrieval:
    def try_fetch(self, word: str, what: str):
        html_content = self.try_fetch_local(word, what)
        if html_content is None:
            html_content = self.fetch_web(word, what)

        return html_content

    def fetch_web(self, word, what: str):
        fetcher = html_fetcher.WebHtmlFetcher(word)
        html_content = fetcher.fetch(what)
        return html_content

    def try_fetch_local(self, word, what: str):
        fetcher = html_fetcher.LocalHtmlFetcher(word)
        try:
            html_content = fetcher.fetch(what)
        except FileNotFoundError:
            return None
        else:
            return html_content

    def get_def_content(self, word: str):
        html_content = self.try_fetch(word, "def")
        # TODO: save html

        parser = HtmlParser()
        def_content = parser.parse(word, html_content)
        learn_content = parser.parse_learn(word, html_content)

        return def_content, learn_content

    def get_syn_content(self, word: str):
        html_content = self.try_fetch(word, "syn")
        # TODO: save html

        parser = HtmlParser()
        return parser.parse_syn(word, html_content)
