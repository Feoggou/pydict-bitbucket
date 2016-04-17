import os
import json
import re

from enum import Enum

from . import colors


class SearchIn(Enum):
    invalid = 0,
    definitions = 1
    examples = 2


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

        self._get_items = {SearchIn.definitions: JsonSearch._def_gatherer,
                           SearchIn.examples: JsonSearch._ex_gatherer}

    @staticmethod
    def _def_gatherer(obj):
        return JsonSearch._get_semantics(obj) + JsonSearch._get_defs(obj) + JsonSearch._get_translations(obj)

    @staticmethod
    def _ex_gatherer(obj):
        return JsonSearch._get_ex(obj) + JsonSearch._get_translations(obj)

    @staticmethod
    def _get_semantics(obj: dict):
        return [x["semantics"] for x in obj["def_groups"] if "semantics" in x.keys()]

    @staticmethod
    def _get_all_defs(group):
        items = []

        for definition in group:
            if "def" in definition.keys():
                items.append(definition["def"])

            elif "def_subgroup" in definition.keys():
                items += JsonSearch._get_all_defs(definition["def_subgroup"])

        return items

    @staticmethod
    def _get_all_examples(group):
        items = []

        for definition in group:
            if "example" in definition.keys():
                items.append(definition["example"])

            elif "def_subgroup" in definition.keys():
                items += JsonSearch._get_all_examples(definition["def_subgroup"])

        return items

    @staticmethod
    def _get_defs(obj: dict):
        items = []

        for x in obj["def_groups"]:
            for ggroup in x["gram_groups"]:
                items += JsonSearch._get_all_defs(ggroup["defs"])

        return items

    @staticmethod
    def _get_ex(obj: dict):
        items = []

        for x in obj["def_groups"]:
            for ggroup in x["gram_groups"]:
                items += JsonSearch._get_all_examples(ggroup["defs"])

        return items

    @staticmethod
    def _get_translations(obj: dict):
        items = []
        if "translations" in obj.keys():
            trans_list = ["[transl.] " + x for x in obj["translations"]]
            items += trans_list
        return items

    @staticmethod
    def _sort_unique_items(items: list):
        items = sorted(list(set(items)), reverse=True)
        return items

    def search_files(self) -> list:
        all_files = [x for x in os.listdir(self.dir_path) if x.endswith(".json")]
        return all_files

    @staticmethod
    def _find_content_in_list(word, items):
        # i.e. matters lowercase, and must be whole word (without " " or "-")
        pattern = re.compile(r'\b{}\b'.format(word))
        results = [x for x in items if re.search(pattern, x)]

        return results

    def _search_json(self, obj: dict, word_name: str):
        items = self._get_items[self._in](obj)

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

    def search_examples(self):
        all_files = self.search_files()

        contents = []
        for file in all_files:
            content = self.search_content(file)
            contents.append(content)

        contents = self.process_contents(contents)

        return contents
