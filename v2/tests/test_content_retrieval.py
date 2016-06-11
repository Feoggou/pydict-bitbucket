import json
import os

import unittest
from unittest import mock
from unittest.mock import  patch, call

from src.content_retrieval import ContentRetrieval
from src.html_fetcher import HtmlFetcher
from src.html_parser import HtmlParser


class ContentRetrievalTest(unittest.TestCase):
    expected_json = None
    html_content = None

    @classmethod
    def setUpClass(cls):
        with open('expected_do.def') as f:
            cls.expected_json = json.load(f)

        path = os.path.dirname(os.path.abspath(__file__))

        with open(os.path.join(path, "do", "do_defs.html")) as f:
            cls.html_content = f.read()

    def test_getContentDef_do(self):
        """
        input: word to retrieve
        result: content for do.
        """
        # must:
        # a. fetch html
        # b. transform to json (parse)
        with patch.object(HtmlFetcher, 'fetch') as mock_fetch:
            mock_fetch.return_value = ContentRetrievalTest.html_content

            with patch.object(HtmlParser, 'parse') as mock_parser:
                mock_parser.return_value = ContentRetrievalTest.expected_json

                content_retrieval = ContentRetrieval()
                result = content_retrieval.get_def_content()

        mock_fetch.assert_called_once_with("do")
        mock_parser.assert_called_once_with(ContentRetrievalTest.html_content)
        self.assertEqual(ContentRetrievalTest.expected_json, result)


if __name__ == '__main__':
    unittest.main()
