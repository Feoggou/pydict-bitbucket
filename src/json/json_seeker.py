import os
import json
import re
import unicodedata

from collections import OrderedDict


from .. import colors
from .json_item_gatherer import SearchIn, ItemGatherer


class SearchResult:
    def __init__(self, word: str, items: list):
        self.items = items
        self.word = word

    def file_item_to_text(self, item: dict):
        file_name = list(item)[0]
        text = "{}[{}]{}\n".format(colors.BOLDBLACK, file_name, colors.RESET)

        for line in item[file_name]:
            line_text = "o) " + line + "\n"
            line_text = line_text.replace(self.word, colors.BOLDRED + self.word + colors.RESET)
            text += line_text

        return text

    def _to_text(self, items):
        text = ""
        for file_item in items:
            text += self.file_item_to_text(file_item) + "\n"

        return text + "\n"

    def __str__(self):
        return self._to_text(self.items)


class SearchAllResult(SearchResult):
    def __init__(self, word: str, items: list):
        SearchResult.__init__(self, word, items)

    def __str__(self):
        text = "\n"

        keys = list(self.items)

        for key in keys:
            text += colors.BOLDBLUE + "=== " + str(key).upper() + " ===\n" + colors.RESET
            if key == "files":
                text += "\n".join(self.items[key]) + "\n\n"
            else:
                text += self._to_text(self.items[key])

        return text


class JsonSearch:
    def __init__(self, dir_path: str, what: str, search_in: SearchIn):
        self.dir_path = dir_path
        self.what = what
        self._in = search_in

    @staticmethod
    def _sort_unique_items(items: list):
        items = sorted(list(set(items)), reverse=True)
        return items

    def list_json_files(self) -> list:
        all_files = [x for x in os.listdir(self.dir_path) if x.endswith(".json")]
        return all_files

    @staticmethod
    def _find_content_in_list(word, items):
        # case insensitive, whole word if "word" is one word
        # otherwise - if word contains "-", " ", "'", simply search in.
        lower_word = word.lower()

        if re.search('[\- \.\']', lower_word):
            results = [x for x in items if lower_word in (x.replace(" ", "-").lower())]
        else:
            pattern = re.compile(r'\b%s\b' % lower_word)
            results = [x for x in items if re.search(pattern, x.lower())]

        return results

    def _search_json(self, obj: dict, word_name: str):
        gatherer = ItemGatherer()
        items = gatherer.get_items[self._in](obj)

        sorted_items = JsonSearch._sort_unique_items(items)
        results = JsonSearch._find_content_in_list(word_name, sorted_items)
        return results

    def search_content(self, file: str) -> dict:
        file_name = os.path.join(self.dir_path, file)

        with open(file_name, "r", encoding="utf-8") as json_file:
            # TODO --- utf-8 everywhere where open() is used + tests.
            text = json_file.read()
            text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode("ascii")
            obj = json.loads(text)

        items = self._search_json(obj, self.what)
        return {file: items} if len(items) else {}

    @staticmethod
    def process_contents(contents: list) -> list:
        contents = [x for x in contents if x != {}]
        contents.sort(key=lambda x: list(x.keys())[0])
        return contents

    def __call__(self, *args, **kwargs):
        all_files = self.list_json_files()

        contents = []
        for file in all_files:
            content = self.search_content(file)
            contents.append(content)

        contents = self.process_contents(contents)

        return contents

    def _search_files(self):
        all_files = self.list_json_files()
        all_words = [x.replace(".json", "") for x in all_files]

        matched_words = self._find_content_in_list(self.what, all_words)
        return [x + ".json" for x in matched_words]

    def _search_word_forms(self):
        self._in = SearchIn.word_forms
        return self.__call__()

    def _search_synonyms(self):
        self._in = SearchIn.synonyms
        return self.__call__()

    def _search_related(self):
        self._in = SearchIn.related
        return self.__call__()

    def _search_defs(self):
        self._in = SearchIn.definitions_simple
        return self.__call__()

    def _search_examples(self):
        self._in = SearchIn.examples_simple
        return self.__call__()

    def _search_semantics(self):
        self._in = SearchIn.semantics
        return self.__call__()

    def _search_translations(self):
        self._in = SearchIn.translations
        return self.__call__()

    def _search_categories(self):
        self._in = SearchIn.categories
        return self.__call__()

    def search_all(self):
        files = self._search_files()
        word_forms = self._search_word_forms()
        syns = self._search_synonyms()
        related = self._search_related()
        defs = self._search_defs()
        examples = self._search_examples()
        semantics = self._search_semantics()
        translations = self._search_translations()
        categories = self._search_categories()

        json_obj = OrderedDict()
        if len(files):
            json_obj["files"] = files

        if len(word_forms):
            json_obj["word forms"] = word_forms

        if len(syns):
            json_obj["synonyms"] = syns

        if len(related):
            json_obj["related / nearby"] = related

        if len(defs):
            json_obj["definitions"] = defs

        if len(examples):
            json_obj["examples"] = examples

        if len(semantics):
            json_obj["semantics"] = semantics

        if len(translations):
            json_obj["translations"] = translations

        if len(categories):
            json_obj["categories"] = categories

        return json_obj
