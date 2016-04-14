import os
import json
import re

from . import dict_cmd
from .dict_cmd import Command, Parameter
from .json_reader import JsonReader


class ListCommand(Command):
    def __init__(self, what: str):
        Command.__init__(self)
        self.dir_path = ""
        self.what = what
        if what == "":
            self.what = None

    @staticmethod
    def get_name() -> str:
        return "list"

    @staticmethod
    def get_alias() -> str:
        return ""

    @staticmethod
    def get_description(cmd_name: str = "") -> str:
        assert cmd_name is None or len(cmd_name) == 0
        return "lists all the words in the def. dir matching pattern."

    @staticmethod
    def get_argument_info() -> Parameter:
        return None

    def set_dir_path(self, dir_path):
        self.dir_path = dir_path

    def execute(self):
        all_words = [x.replace(".json", "") for x in os.listdir(self.dir_path) if x.endswith(".json")]

        if self.what is not None:
            pattern = re.compile(r'{}'.format(self.what))
            words = [x for x in all_words if re.search(pattern, x)]
        else:
            words = all_words

        text = "\n".join(words) + "\n\n"
        text += "total: " + str(len(words))

        return text


dict_cmd.CMD_CLASSES.append(ListCommand)

