from . import dict_cmd
from .dict_cmd import Command, Parameter
from . import json_seeker


class ExCommand(Command):
    def __init__(self, what: str):
        Command.__init__(self)
        self.dir_path = ""
        self.what = what
        if what == "":
            self.what = None

    @staticmethod
    def get_name() -> str:
        return "ex"

    @staticmethod
    def get_alias() -> str:
        return ""

    @staticmethod
    def get_description(cmd_name: str = "") -> str:
        assert cmd_name is None or len(cmd_name) == 0
        text = "search all .json files, and print all examples that\n"
        text += " " * 14 + "contain the word <word>"

        return text

    @staticmethod
    def get_argument_info() -> Parameter:
        return None

    def set_dir_path(self, dir_path):
        self.dir_path = dir_path

    def execute(self):
        seeker = json_seeker.JsonSearch(self.dir_path, self.what, json_seeker.SearchIn.examples)
        json_obj = seeker()

        text_obj = json_seeker.SearchResult(self.what, json_obj)
        return text_obj


dict_cmd.CMD_CLASSES.append(ExCommand)

