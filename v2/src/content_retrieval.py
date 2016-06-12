from .html_fetcher import WebHtmlFetcher, LocalHtmlFetcher
from .html_parser import HtmlParser


class ContentRetrieval:
    def __init__(self, from_web: bool):
        self.Fetcher = WebHtmlFetcher if from_web else LocalHtmlFetcher

    def get_def_content(self):
        fetcher = self.Fetcher("do")
        html_content = fetcher.fetch()
        # TODO: save html

        parser = HtmlParser()
        return parser.parse("do", html_content)

    def get_syn_content(self):
        fetcher = self.Fetcher("do")
        html_content = fetcher.fetch_syn()
        # TODO: save html

        parser = HtmlParser()
        return parser.parse_syn("do", html_content)
