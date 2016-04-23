import os
import json

from . import dict_cmd
from .dict_cmd import Command, Parameter
from .json_reader import JsonReader


class PrintCommand(Command):
    def __init__(self, word_name: str):
        Command.__init__(self)
        self.dir_path = ""
        self.word = word_name

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

    def execute(self):
        file_name = os.path.join(self.dir_path, self.word + ".json")

        if not os.path.exists(file_name):
            print("Word '{}' does not exist!".format(self.word))
            return ""

        with open(file_name, "r") as json_file:
            content = json.load(json_file)

        return self.read_content(self.word, content)

    def read_content(self, word: str, content: dict) -> str:
        reader = JsonReader(content)
        return reader.read_content(word)


dict_cmd.CMD_CLASSES.append(PrintCommand)

