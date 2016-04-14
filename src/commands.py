import re

from .dict_cmd import *

from .cmd_getword import GetWordCommand
from . import cmd_help
from . import cmd_quit
from . import cmd_print
from . import cmd_nearby
from . import cmd_related


def get_command(cmd_name: str, cmd_arg: str=None) -> Command:
    if cmd_arg == "":
        cmd_arg = None

    if cmd_name is None or len(cmd_name) == 0:
        raise ValueError("in_str should not be empty / None!")

    for command in CMD_CLASSES:
        if cmd_name == command.get_name() or cmd_name == command.get_alias():
            return command(cmd_arg)


def match_default_command(in_str: str) -> Command:
    if in_str is None or len(in_str) == 0:
        raise ValueError("in_str should not be empty / None!")

    match = re.match(r'[A-Za-z0-9\- \.\']+', in_str)
    if match is None:
        raise ValueError("Invalid word: '{}'".format(in_str))

    cmd = GetWordCommand()
    return cmd


def match_command(in_str: str, dir_path: str="") -> Command:
    if in_str is None or len(in_str) == 0:
        raise ValueError("in_str should not be empty / None!")

    match = re.match(r'([a-z]+)\((.*)\)', in_str)

    if match is None:
        return match_default_command(in_str)

    cmd_name = match.groups()[0]
    cmd_arg = match.groups()[1]

    cmd = get_command(cmd_name, cmd_arg)
    cmd.set_dir_path(dir_path)

    return cmd
