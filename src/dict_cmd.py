

class Parameter:
    def __init__(self, name: str, required: bool):
        self.name = name
        self.required = required


class Command:
    def __init__(self):
        pass

    @staticmethod
    def get_name() -> str:
        raise NotImplementedError()

    @staticmethod
    def get_alias() -> str:
        raise NotImplementedError()

    @staticmethod
    def get_description(cmd_name: str = "") -> str:
        raise NotImplementedError()

    @staticmethod
    def get_argument() -> Parameter:
        raise NotImplementedError()

    def execute(self) -> str:
        raise NotImplementedError()


CMD_CLASSES = []


def get_command(in_str: str) -> Command:
    if in_str is None or len(in_str) == 0:
        raise ValueError("in_str should not be empty / None!")

    for command in CMD_CLASSES:
        if in_str == command.get_name() or in_str == command.get_alias():
            return command()

from . import cmd_help
from . import cmd_quit