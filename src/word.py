import http.client
import os
import re

from .html_parser.def_groups import *
from .html_parser.syn_groups import *
from .html_parser.rel_groups import *

HTML_PATH = "/home/zenith/PycharmProjects/EDictionary/html"

class RedirectError(Exception):
    def __init__(self, value: str):
        self.value = value


class WordData:
    def __init__(self, word_name):
        self.word_name = word_name
        self.def_content = ""
        self.related_content = ""
        self.synonyms_content = ""

    @staticmethod
    def _fetch_from_web(suffix):
        data = suffix.encode("utf-8")
        txt = data.decode("ascii", errors="backslashreplace")
        txt = txt.replace("\\x", "%")
        suffix = txt

        hostname = "www.collinsdictionary.com"
        conn = http.client.HTTPConnection(hostname)
        # print("from " + hostname + "/dictionary/" + suffix)
        conn.request("GET", "/dictionary/" + suffix)
        reason = conn.getresponse()

        data = reason.read()
        text = data.decode()

        if len(text) == 0:
            redirect_loc = reason.getheader('location')
            if redirect_loc is not None:
                redir_word = redirect_loc.split('/')[-1]
                raise RedirectError(redir_word)

        return text

    def _fetch_from_web_dict(self, suffix):
        return self._fetch_from_web("american/" + suffix)

    def _fetch_web_thesaurus(self, suffix):
        return self._fetch_from_web("american-thesaurus/" + suffix)

    def fetch(self):
        print(self.word_name + "...")
        self.def_content = self._fetch_from_web_dict(self.word_name)
        if len(self.def_content) == 0:
            return

        with open(os.path.join(HTML_PATH, self.word_name + ".html"), "w") as f:
            f.write(self.def_content)

        try:
            self.related_content = self._fetch_from_web_dict(self.word_name + "/related")
        except RedirectError as e:
            if re.match("american\?q=.*", e.value):
                print("(no related)")
            else:
                print("related: ignored redirect '{}'".format(e.value))
        except:
            raise
        else:
            with open(os.path.join(HTML_PATH, self.word_name + "-related.html"), "w") as f:
                f.write(self.related_content)

        try:
            self.synonyms_content = self._fetch_web_thesaurus(self.word_name)
        except RedirectError as e:
            if re.match("american-thesaurus\?q=.*", e.value):
                print("(no synonyms)")
            else:
                print("synonyms: ignored redirect '{}'".format(e.value))
        except:
            raise
        else:
            with open(os.path.join(HTML_PATH, self.word_name + "-syn.html"), "w") as f:
                f.write(self.synonyms_content)

    def fetch_mock(self):
        f = open("{}_defs.html".format(self.word_name))
        self.def_content = f.read()

        related = "{}_related.html".format(self.word_name)
        if os.path.exists(related):
            f = open(related)
            self.related_content = f.read()

        synonyms = "{}_syn.html".format(self.word_name)
        if os.path.exists(synonyms):
            f = open(synonyms)
            self.synonyms_content = f.read()

    def download_definition(self) -> str:
        return self._fetch_from_web_dict(self.word_name)

    def build_content(self) -> dict:
        if len(self.def_content) == 0:
            return None

        obj = HtmlToJson(self.word_name, self.def_content)
        content = obj.translate()

        if len(self.synonyms_content) > 0:
            synonyms = HtmlToJsonSynonyms(self.word_name, self.synonyms_content)
            content["synonyms"] = synonyms.translate()

        if len(self.related_content) > 0:
            related = HtmlToJsonRelated(self.related_content)
            text = related.translate()
            if len(text):
                content["related_words"] = text

        return content
