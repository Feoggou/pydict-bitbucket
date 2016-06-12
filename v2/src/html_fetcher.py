import http
from http import client
import os

from src import config


class WordNotFoundError(RuntimeError):
    def __init__(self, word_name):
        self.value = word_name

    def __str__(self):
        return repr(self.value)


class LocalHtmlFetcher:
    def __init__(self, word: str):
        self.word = word

    def fetch(self):
        with open(os.path.join(config.HTML_DIR_PATH, self.word + "_defs.html"), "r") as f:
            return f.read()

    def fetch_syn(self):
        with open(os.path.join(config.HTML_DIR_PATH, self.word + "_syn.html"), "r") as f:
            return f.read()


class WebHtmlFetcher:
    def __init__(self, word: str):
        self.word = word

    def fetch(self):
        reason, text = self._try_fetch(config.HTTP_PATH)

        if len(text) == 0:
            return self._handle_error(reason)

        return text

    def fetch_syn(self):
        reason, text = self._try_fetch(config.SYN_HTTP_PATH)

        if len(text) == 0:
            return self._handle_error(reason)

        return text

    def _try_fetch(self, http_path):
        conn = http.client.HTTPConnection(config.HOSTNAME)
        conn.request("GET", http_path + self.word)
        reason = conn.getresponse()

        data = reason.read()
        text = data.decode()

        return reason, text

    def _handle_error(self, reason):
        redirect_loc = reason.getheader('location')
        assert redirect_loc is not None

        if self._is_word_not_found(redirect_loc):
            raise WordNotFoundError(self.word)

        self._update_redirect_word(redirect_loc)
        return self.fetch()

    def _update_redirect_word(self, redirect_loc):
        self.word = redirect_loc.split('/')[-1]

    @staticmethod
    def _is_word_not_found(redirect_item: str) -> bool:
        return redirect_item.split('/')[1] == "spellcheck"


class HtmlFetcher:
    def fetch(self, word: str):
        raise NotImplementedError()
