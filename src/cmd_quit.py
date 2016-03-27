from . import dict_cmd
from .dict_cmd import Command, Parameter


class QuitCommand(Command):
    def __init__(self):
        Command.__init__(self)
        pass

    @staticmethod
    def get_name() -> str:
        return "quit"

    @staticmethod
    def get_alias() -> str:
        return "exit"

    @staticmethod
    def get_description(cmd_name: str = "") -> str:
        assert cmd_name is None or len(cmd_name) == 0
        return "exit the script"

    @staticmethod
    def get_argument() -> Parameter:
        return None

    def execute(self):
        """exit the script"""
        exit(0)


dict_cmd.CMD_CLASSES.append(QuitCommand)

