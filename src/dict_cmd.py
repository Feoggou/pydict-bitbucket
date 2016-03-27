import re


class Parameter:
    def __init__(self, name: str, required: bool):
        self.name = name
        self.required = required
        self.value = None


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
    def get_argument_info() -> Parameter:
        raise NotImplementedError()

    def set_argument_value(self, v: str):
        raise NotImplementedError()

    def get_argument_value(self) -> str:
        raise NotImplementedError()

    def execute(self) -> str:
        raise NotImplementedError()


class DefaultCommand(Command):
    def set_argument_value(self, v: str):
        pass


CMD_CLASSES = []


def get_command(in_str: str) -> Command:
    if in_str is None or len(in_str) == 0:
        raise ValueError("in_str should not be empty / None!")

    for command in CMD_CLASSES:
        if in_str == command.get_name() or in_str == command.get_alias():
            return command()


def match_default_command(in_str: str) -> Command:
    if in_str is None or len(in_str) == 0:
        raise ValueError("in_str should not be empty / None!")

    match = re.match(r'[A-Za-z0-9\- \.\']+', in_str)
    if match is None:
        raise ValueError("Invalid word: '{}'".format(in_str))

    cmd = DefaultCommand()
    cmd.set_argument_value(in_str)
    return cmd


def match_command(in_str: str) -> Command:
    if in_str is None or len(in_str) == 0:
        raise ValueError("in_str should not be empty / None!")

    match = re.match(r'([a-z]+)\((.*)\)', in_str)

    if match is None:
        return match_default_command(in_str)

    cmd_name = match.groups()[0]
    cmd_arg = match.groups()[1]

    cmd = get_command(cmd_name)
    if len(cmd_arg):
        cmd.set_argument_value(cmd_arg)

    return cmd


from . import cmd_help
from . import cmd_quit