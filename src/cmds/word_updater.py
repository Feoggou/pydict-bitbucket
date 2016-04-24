import os
import json

import difflib

from .cmd_getword import WordInvalidError
from . import cmd_getword

from .word_handler import WordHandler
from ..json.json_reader import JsonReader
from .. import colors


def output_msg(args):
    print(args)


class WordUpdater:
    def __init__(self, dir_path: str):
        self.dir_path = dir_path

    def _exists(self, word: str) -> bool:
        file_path = os.path.join(self.dir_path, word + ".json")
        exists = os.path.exists(file_path)
        return exists

    @staticmethod
    def update_new_with_old_my(old_content: dict, new_content: dict) -> bool:
        if "my_examples" in old_content.keys():
            new_content["my_examples"] = old_content["my_examples"]

        if "subwords" in old_content.keys():
            new_content["subwords"] = old_content["subwords"]

            for subword in new_content["subwords"]:
                if not new_content["subwords"][subword]:
                    WordHandler.remove_subword(new_content, subword)

    def _overwrite_json(self, word: str, content: dict):
        file_path = os.path.join(self.dir_path, word)
        file_path += ".json"

        os.remove(file_path)

        with open(file_path, "w") as f:
            json.dump(content, f, indent=4, sort_keys=True)

    @staticmethod
    def _get_word_definition(word):
        cmd = cmd_getword.GetWordCommand()

        answer = "yes"

        while answer.lower() == "yes":
            try:
                json_content = cmd.execute(word)
            except WordInvalidError as e:
                output_msg(str(e))
                return None
            else:
                return json_content

    @staticmethod
    def print_differences(word, old_content: dict, new_content: dict):
        reader = JsonReader(old_content, use_colors=False)
        old_text = reader.read_content(word)

        reader = JsonReader(new_content, use_colors=False)
        new_text = reader.read_content(word)

        result = difflib.unified_diff(old_text.splitlines(), new_text.splitlines())
        for line in result:
            if line[0] == "+":
                line = colors.GREEN + line + colors.RESET
            elif line[0] == "-":
                line = colors.RED + line + colors.RESET
            elif line.startswith("@@"):
                line = colors.YELLOW + line + colors.RESET
            print(line)

    def __call__(self, word: str):
        if not self._exists(word):
            print("cannot update word '{}' - it does not exist locally!".format(word))
            return

        new_content = self._get_word_definition(word)

        file_path = os.path.join(self.dir_path, word + ".json")
        with open(file_path, "r") as f:
            old_content = json.load(f)

        self.update_new_with_old_my(old_content, new_content)
        self._overwrite_json(word, new_content)

        self.print_differences(word, old_content, new_content)

        return ""

