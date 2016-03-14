import html_to_json
import http.client


class WordData:
    def __init__(self, word_name):
        self.word_name = word_name
        self.def_content = ""
        self.related_content = ""
        self.synonyms_content = ""

    def _fetch_from_web(self, suffix):
        hostname = "www.collinsdictionary.com"
        conn = http.client.HTTPConnection(hostname)
        conn.request("GET", "/dictionary/" + suffix)
        reason = conn.getresponse()
        data = reason.read()
        text = data.decode()
        return text

    def _fetch_from_web_dict(self, suffix):
        return self._fetch_from_web("american/" + suffix)

    def _fetch_web_thesaurus(self, suffix):
        return self._fetch_from_web("american-thesaurus/" + suffix)

    def fetch(self):
        print("real fetch!")
        self.def_content = self._fetch_from_web_dict(self.word_name)
        self.related_content = self._fetch_from_web_dict(self.word_name + "/related")
        self.synonyms_content = self._fetch_web_thesaurus(self.word_name)

    def fetch_mock(self):
        f = open("file.htm")
        self.def_content = f.read()

        f = open("do_related.html")
        self.related_content = f.read()

        f = open("do_syn.html")
        self.synonyms_content = f.read()

    def download_definition(self) -> str:
        return self._fetch_from_web_dict(self.word_name)

    def build_content(self) -> dict:
        obj = html_to_json.HtmlToJson(self.word_name, self.def_content)
        content = obj.translate()

        synonyms = html_to_json.HtmlToJsonSynonyms(self.word_name, self.synonyms_content)
        content["word"].append(synonyms.translate())

        # related
        related = html_to_json.HtmlToJsonRelated(self.related_content)
        content["word"].append(related.translate())

        return content