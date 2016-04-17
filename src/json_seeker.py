import os
import json
import re


from . import colors
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

    def __str__(self):
        text = ""
        for file_item in self.items:
            text += self.file_item_to_text(file_item) + "\n"

        return text + "\n"


class JsonSearch:
    def __init__(self, dir_path: str, what: str, search_in: SearchIn):
        self.dir_path = dir_path
        self.what = what
        self._in = search_in

    @staticmethod
    def _sort_unique_items(items: list):
        items = sorted(list(set(items)), reverse=True)
        return items

    def search_files(self) -> list:
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

        with open(file_name, "r") as json_file:
            obj = json.load(json_file)

        items = self._search_json(obj, self.what)
        return {file: items} if len(items) else {}

    @staticmethod
    def process_contents(contents: list) -> list:
        contents = [x for x in contents if x != {}]
        contents.sort(key=lambda x: list(x.keys())[0])
        return contents

    def __call__(self, *args, **kwargs):
        all_files = self.search_files()

        contents = []
        for file in all_files:
            content = self.search_content(file)
            contents.append(content)

        contents = self.process_contents(contents)

        return contents
