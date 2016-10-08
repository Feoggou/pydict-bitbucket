import unittest
from unittest import mock
from unittest.mock import patch

from src.content_retrieval import ContentRetrieval
from src.html_fetcher import HtmlFetcher
from src.html_parser import HtmlParser


class ContentRetrievalTest(unittest.TestCase):
    def test_getContentDef_tall_retrievesContent(self):
        """
        input: word to retrieve
        result: content for tall.
        """

        exp_json = "dummy_value"
        html_content = "dummy_html_content"

        # must:
        # a. fetch html
        # b. transform to json (parse)
        with patch.object(HtmlFetcher, 'fetch') as mock_fetch:
            mock_fetch.return_value = html_content
            with patch.object(HtmlParser, 'parse') as mock_parser:
                mock_parser.return_value = exp_json
                with patch.object(HtmlParser, 'parse_learn'):
                    content_retrieval = ContentRetrieval()
                    result, learn_content = content_retrieval.get_def_content("tall")

        mock_fetch.assert_called_once_with(mock.ANY)
        mock_parser.assert_called_once_with("tall", html_content)

        self.assertEqual(exp_json, result)

    def test_do_findInLocal_getFromLocal(self):
        exp_json = "dummy_value"
        html_content = "dummy_html_content"

        with patch.object(HtmlFetcher, 'fetch') as mock_fetch:
            mock_fetch.return_value = html_content
            with patch.object(HtmlParser, 'parse') as mock_parser:
                mock_parser.return_value = exp_json
                with patch.object(HtmlParser, 'parse_learn'):
                    content_retrieval = ContentRetrieval()
                    result, learn_content = content_retrieval.get_def_content("do")

        self.assertEqual(exp_json, result)
        mock_fetch.assert_called_once_with(mock.ANY)

    def test_do_notFoundInLocal_getFromWeb(self):
        exp_json = "dummy_value"
        html_content = "dummy_html_content"

        # TODO: Was LocalHtmlFetcher, then WebHtmlFetcher
        with patch.object(HtmlFetcher, 'fetch') as mock_fetch_web:
            mock_fetch_web.side_effect = FileNotFoundError("No such file or directory")
            with patch.object(HtmlFetcher, 'fetch') as mock_fetch_web:
                mock_fetch_web.return_value = html_content
                with patch.object(HtmlParser, 'parse') as mock_parser:
                    mock_parser.return_value = exp_json
                    with patch.object(HtmlParser, 'parse_learn'):
                        content_retrieval = ContentRetrieval()
                        result, learn_content = content_retrieval.get_def_content("do")

        self.assertEqual(exp_json, result)
        mock_fetch_web.assert_called_once_with(mock.ANY)

    def test_get_tall_syn(self):
        exp_json = "dummy_value"
        html_content = "dummy_html_content"

        with patch('src.html_fetcher.HtmlFetcher', autospec=True) as MockLocalHtmlFetcher:
            mock_fetch_obj = MockLocalHtmlFetcher.return_value
            mock_fetch_obj.fetch.return_value = html_content

            with patch.object(HtmlParser, 'parse_syn') as mock_parser:
                mock_parser.return_value = exp_json
                content_retrieval = ContentRetrieval()
                result = content_retrieval.get_syn_content("tall")

        self.assertEqual(exp_json, result)
        mock_fetch_obj.fetch.assert_called_once_with("syn")
        MockLocalHtmlFetcher.assert_called_once_with("tall")


if __name__ == '__main__':
    unittest.main()
