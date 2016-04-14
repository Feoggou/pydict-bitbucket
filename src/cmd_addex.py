import os
import json

from . import dict_cmd
from .dict_cmd import Command, Parameter


class AddExCommand(Command):
    def __init__(self, word: str):
        Command.__init__(self)
        self.dir_path = ""
        self.word = word

    @staticmethod
    def get_name() -> str:
        return "addex"

    @staticmethod
    def get_alias() -> str:
        return ""

    @staticmethod
    def get_description(cmd_name: str = "") -> str:
        assert cmd_name is None or len(cmd_name) == 0
        return "add an example json object into the .json file"

    @staticmethod
    def get_argument_info() -> Parameter:
        return None

    def set_dir_path(self, dir_path):
        self.dir_path = dir_path

    def execute(self):
        if self.word is None or len(self.word) == "":
            raise ValueError("Word not provided to command addex!")

        json_file_name = self.dir_path + "/" + self.word + ".json"

        if not os.path.exists(json_file_name):
            print("word '{}' does not exist!".format(self.word))
            return ""

        with open(json_file_name, "r") as json_file:
            obj = json.load(json_file)

        example_value = input("example: ")
        obj["examples"].append({"example": example_value})

        with open(json_file_name, "w") as json_file:
            json.dump(obj, json_file, indent=4, sort_keys=True)

        return ""


dict_cmd.CMD_CLASSES.append(AddExCommand)

