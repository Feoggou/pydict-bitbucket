import http.client
import os

from .def_groups import  *
from .syn_groups import  *
from .rel_groups import  *


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
        hostname = "www.collinsdictionary.com"
        conn = http.client.HTTPConnection(hostname)
        print("from " + hostname + "/dictionary/" + suffix)
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
        print("fetching...")
        self.def_content = self._fetch_from_web_dict(self.word_name)
        if len(self.def_content) == 0:
            return

        try:
            self.related_content = self._fetch_from_web_dict(self.word_name + "/related")
        except RedirectError as e:
            print("ignored redirect related: ", e.value)
        except:
            raise

        try:
            self.synonyms_content = self._fetch_web_thesaurus(self.word_name)
        except RedirectError as e:
            print("ignored redirect syn: ", e.value)
        except:
            raise

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
