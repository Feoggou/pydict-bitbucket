import os
import json

from . import dict_cmd
from .dict_cmd import Command, Parameter


class PrintCommand(Command):
    def __init__(self):
        Command.__init__(self)
        self.dir_path = ""

    @staticmethod
    def get_name() -> str:
        return "print"

    @staticmethod
    def get_alias() -> str:
        return ""

    @staticmethod
    def get_description(cmd_name: str = "") -> str:
        assert cmd_name is None or len(cmd_name) == 0
        return "print all info from json in textual format"

    @staticmethod
    def get_argument_info() -> Parameter:
        return None

    def set_dir_path(self, dir_path):
        self.dir_path = dir_path

    def execute(self, word: str):
        file_name = os.path.join(self.dir_path, word + ".json")

        with open(file_name, "r") as json_file:
            content = json.load(json_file)

        self._print_content(content)
        return None

    def _print_content(self, content: dict):
        self._frequency_to_text(content)
        self._definitions_to_text(content)
        self._translations_to_text(content)
        self._synonyms_to_text(content)
        self._examples_to_text(content)

    def _frequency_to_text(self, content: dict):
        raise NotImplementedError

    def _definitions_to_text(self, content: dict):
        raise NotImplementedError

    def _translations_to_text(self, content: dict):
        raise NotImplementedError

    def _synonyms_to_text(self, content: dict):
        raise NotImplementedError

    def _examples_to_text(self, content: dict):
        raise NotImplementedError


dict_cmd.CMD_CLASSES.append(PrintCommand)

