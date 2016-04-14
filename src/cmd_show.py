import os
import json

from . import dict_cmd
from .dict_cmd import Command, Parameter
from .json_reader import JsonReader


class ShowCommand(Command):
    def __init__(self, word_name: str):
        Command.__init__(self)
        self.dir_path = ""
        self.word = word_name

    @staticmethod
    def get_name() -> str:
        return "show"

    @staticmethod
    def get_alias() -> str:
        return ""

    @staticmethod
    def get_description(cmd_name: str = "") -> str:
        assert cmd_name is None or len(cmd_name) == 0
        return "show the json file for the word"

    @staticmethod
    def get_argument_info() -> Parameter:
        return None

    def set_dir_path(self, dir_path):
        self.dir_path = dir_path

    def execute(self):
        file_name = os.path.join(self.dir_path, self.word + ".json")

        with open(file_name, "r") as json_file:
            content = json.load(json_file)

        return json.dumps(content, indent=2, sort_keys=True)  #  str(content)


dict_cmd.CMD_CLASSES.append(ShowCommand)

