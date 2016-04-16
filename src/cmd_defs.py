import os
import json
import re

from . import dict_cmd
from .dict_cmd import Command, Parameter
from . import colors


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


class DefsCommand(Command):
    def __init__(self, what: str):
        Command.__init__(self)
        self.dir_path = ""
        self.what = what
        if what == "":
            self.what = None

    @staticmethod
    def get_name() -> str:
        return "defs"

    @staticmethod
    def get_alias() -> str:
        return ""

    @staticmethod
    def get_description(cmd_name: str = "") -> str:
        assert cmd_name is None or len(cmd_name) == 0
        # TODO
        text = "search all .json files, and print all definitions\n" \
               "that contain the word <word>"

        return text

    @staticmethod
    def get_argument_info() -> Parameter:
        return None

    def set_dir_path(self, dir_path):
        self.dir_path = dir_path

    @staticmethod
    def _get_semantics(obj: dict):
        items = [x["semantics"] for x in obj["def_groups"] if "semantics" in x.keys()]

        return items

    @staticmethod
    def _get_all_defs(group):
        items = []

        for definition in group:
            if "def" in definition.keys():
                items.append(definition["def"])

            elif "def_subgroup" in definition.keys():
                items += DefsCommand._get_all_defs(definition["def_subgroup"])

        return items

    @staticmethod
    def _get_defs(obj: dict):
        items = []

        for x in obj["def_groups"]:
            for ggroup in x["gram_groups"]:
                items += DefsCommand._get_all_defs(ggroup["defs"])

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

    @staticmethod
    def _find_content_in_list(word, items):
        # i.e. matters lowercase, and must be whole word (without " " or "-")
        pattern = re.compile(r'\b{}\b'.format(word))
        results = [x for x in items if re.search(pattern, x)]

        return results

    @staticmethod
    def _search_json(obj: dict, word_name: str):
        semantics = DefsCommand._get_semantics(obj)
        defs = DefsCommand._get_defs(obj)
        transls = DefsCommand._get_translations(obj)

        sorted_items = DefsCommand._sort_unique_items(semantics + defs + transls)
        results = DefsCommand._find_content_in_list(word_name, sorted_items)
        return results

    @staticmethod
    def _search_files(dir_path: str) -> list:
        all_files = [x for x in os.listdir(dir_path) if x.endswith(".json")]
        return all_files

    def _search_content(self, file: str, what: str) -> dict:
        # TODO: file should have already contained the path.
        file_name = os.path.join(self.dir_path, file)

        with open(file_name, "r") as json_file:
            obj = json.load(json_file)

        items = self._search_json(obj, what)
        return {file: items} if len(items) else {}

    @staticmethod
    def _process_contents(contents: list) -> list:
        contents = [x for x in contents if x != {}]
        contents.sort(key=lambda x: list(x.keys())[0])
        return contents

    def _search(self):
        all_files = self._search_files(self.dir_path)

        contents = []
        for file in all_files:
            content = self._search_content(file, self.what)
            contents.append(content)

        contents = self._process_contents(contents)

        return contents

    @staticmethod
    def _json_search_to_text(word: str, contents: list):
        result = SearchResult(word, contents)
        return result

    def execute(self):
        json_obj = self._search()

        text_obj = self._json_search_to_text(self.what, json_obj)
        return text_obj


dict_cmd.CMD_CLASSES.append(DefsCommand)

