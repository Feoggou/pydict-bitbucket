import os

import unittest
from unittest import mock
from unittest.mock import patch

from src.html_fetcher import WebHtmlFetcher, WordNotFoundError


class HtmlFetcherTest(unittest.TestCase):
    expected_html = None

    @classmethod
    def setUpClass(cls):
        path = os.path.dirname(os.path.abspath(__file__))

        with open(os.path.join(path, "do", "do_defs.html")) as f:
            cls.expected_html = f.read()

    def test_fetchFromWeb_do_yieldsAContent(self):
        # here it doesn't matter what text it returns, only that it returns something (no error)
        fetcher = WebHtmlFetcher("do")

        result = fetcher.fetch()

        self.assertGreater(len(result), 0)

    def test_fetchFromWeb_adjudicating_finds_adjudicate(self):
        fetcher = WebHtmlFetcher("adjudicating")

        result = fetcher.fetch()

        self.assertGreater(len(result), 0)

    def test_fetchFromWeb_badWord_raisesException(self):
        fetcher = WebHtmlFetcher("lksjdgjksbd")

        with self.assertRaises(WordNotFoundError) as exc:
            fetcher.fetch()

        self.assertEqual(exc.exception.value, "lksjdgjksbd")


if __name__ == '__main__':
    unittest.main()
