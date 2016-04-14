import os
import re

from . import dict_cmd
from .dict_cmd import Command, Parameter


class WhereCommand(Command):
    def __init__(self, what: str = None):
        Command.__init__(self)
        self.dir_path = ""
        if what is not None:
            raise ValueError("where receives no argument!")

    @staticmethod
    def get_name() -> str:
        return "where"

    @staticmethod
    def get_alias() -> str:
        return ""

    @staticmethod
    def get_description(cmd_name: str = "") -> str:
        assert cmd_name is None or len(cmd_name) == 0
        return "displays the path to the words"

    @staticmethod
    def get_argument_info() -> Parameter:
        return None

    def set_dir_path(self, dir_path):
        self.dir_path = dir_path

    def execute(self):
        return self.dir_path


dict_cmd.CMD_CLASSES.append(WhereCommand)

