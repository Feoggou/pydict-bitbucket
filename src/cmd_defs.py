import os
import json

from . import dict_cmd
from .dict_cmd import Command, Parameter


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
    def _search_json(obj: dict):
        raise NotImplementedError()

    @staticmethod
    def _search_files(dir_path: str) -> list:
        all_files = [x for x in os.listdir(dir_path) if x.endswith(".json")]
        return all_files

    def _search_content(self, file: str, what: str) -> dict:
        # TODO: file should have already contained the path.
        file_name = os.path.join(self.dir_path, file)

        with open(file_name, "r") as json_file:
            obj = json.load(json_file)

        results = self._search_json(obj)
        return results

    def _process_contents(self, contents: list) -> list:
        raise NotImplementedError()

    """def _output_contents(self, contents: list):
        raise NotImplementedError()"""

    def execute(self):
        all_files = self._search_files(self.dir_path)

        contents = []
        for file in all_files:
            content = self._search_content(file, self.what)
            contents.append(content)

        contents = self._process_contents(contents)

        return contents
        # return self._output_contents(contents)


dict_cmd.CMD_CLASSES.append(DefsCommand)

