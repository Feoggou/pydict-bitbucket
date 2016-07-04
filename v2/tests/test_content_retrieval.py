import json
import os

import unittest
from unittest import mock
from unittest.mock import patch, call

from src.content_retrieval import ContentRetrieval
from src.html_fetcher import WebHtmlFetcher, LocalHtmlFetcher
from src.html_parser import HtmlParser


class ContentRetrievalTest(unittest.TestCase):
    expected_json = None
    html_content = None
    path_to_html = None

    @classmethod
    def setUpClass(cls):
        with open('expected_do.def') as f:
            cls.expected_json = json.load(f)

        path = os.path.dirname(os.path.abspath(__file__))
        cls.path_to_html = os.path.join(path, "html_files", "do_defs.html")

        with open(cls.path_to_html) as f:
            cls.html_content = f.read()

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
        with patch.object(WebHtmlFetcher, 'fetch') as mock_fetch:
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

        with patch.object(LocalHtmlFetcher, 'fetch') as mock_fetch:
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

        with patch.object(LocalHtmlFetcher, 'fetch') as mock_fetch_web:
            mock_fetch_web.side_effect = FileNotFoundError("No such file or directory")
            with patch.object(WebHtmlFetcher, 'fetch') as mock_fetch_web:
                mock_fetch_web.return_value = html_content
                with patch.object(HtmlParser, 'parse') as mock_parser:
                    mock_parser.return_value = exp_json
                    with patch.object(HtmlParser, 'parse_learn'):
                        content_retrieval = ContentRetrieval()
                        result, learn_content = content_retrieval.get_def_content("do")

        self.assertEqual(exp_json, result)
        mock_fetch_web.assert_called_once_with(mock.ANY)


if __name__ == '__main__':
    unittest.main()
