from .html_fetcher import HtmlFetcher
from .html_parser import HtmlParser


class ContentRetrieval:
    def get_def_content(self):
        fetcher = HtmlFetcher()
        html_content = fetcher.fetch("do")

        parser = HtmlParser()
        return parser.parse(html_content)

    def get_syn_content(self):
        pass
