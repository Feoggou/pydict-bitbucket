import unittest

from src.html_fetcher import HtmlFetcher, WordNotFoundError


class HtmlFetcherTest(unittest.TestCase):
    def test_fetchFromWeb_do_yieldsAContent(self):
        # here it doesn't matter what text it returns, only that it returns something (no error)
        fetcher = HtmlFetcher("do")

        result = fetcher.fetch(what="def")

        self.assertGreater(len(result), 0)

    # TODO: decide if 'finding similar' is still a concern.
    """
        def test_fetchFromWeb_adjudicating_finds_adjudicate(self):
            fetcher = WebHtmlFetcher("adjudicating")

            result = fetcher.fetch(what="def")

            self.assertGreater(len(result), 0)

        def test_fetchFromWeb_badWord_raisesException(self):
            fetcher = WebHtmlFetcher("lksjdgjksbd")

            with self.assertRaises(WordNotFoundError) as exc:
                fetcher.fetch(what="def")

            self.assertEqual(exc.exception.value, "lksjdgjksbd")
    """


if __name__ == '__main__':
    unittest.main()
