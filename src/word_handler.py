from .cmd_getword import WordInvalidError
from . import cmd_getword
from .word import RedirectError

import os
import re
import json


def output_msg(args):
    print(args)


class WordHandler:
    def __init__(self, dir_path: str):
        self.dir_path = dir_path

    def _already_exists(self, word: str) -> bool:
        file_path = os.path.join(self.dir_path, word + ".json")
        exists = os.path.exists(file_path)
        return exists

    def _print_word(self, word: str):
        raise NotImplementedError()

    # not tested: too simple
    def _save_json(self, word: str, content: dict):
        file_path = os.path.join(self.dir_path, word)
        file_path += ".json"

        with open(file_path, "w") as f:
            json.dump(content, f, indent=4, sort_keys=True)

    def _get_word_definition(self, word):
        cmd = cmd_getword.GetWordCommand()

        answer = "yes"

        while answer.lower() == "yes":
            try:
                json_content = cmd.execute(word)
            except WordInvalidError as e:
                output_msg(str(e))
                return None
            except RedirectError as e:
                if re.match("american\?q=.*", e.value):
                    output_msg("The word '{}' was not found!".format(word))
                    return None

                answer = input("Word '{}' not found. Would you like to get word '{}' instead?".format(word, e.value))
                if answer.lower() == "yes":
                    word = e.value
            else:
                self._save_json(word, json_content)
                self._print_word(json_content)
                return json_content

    def get(self, word: str):
        if self._already_exists(word):
            self._print_word(word)
            return

        definition = self._get_word_definition(word)
        return definition

