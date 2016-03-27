from . import dict_cmd
from .dict_cmd import Command, Parameter


class HelpCommand(Command):
    def __init__(self):
        Command.__init__(self)

    @staticmethod
    def get_name() -> str:
        return "help"

    @staticmethod
    def get_alias() -> str:
        return ""

    @staticmethod
    def get_argument() -> Parameter:
        return Parameter("cmd", required=False)

    @staticmethod
    def get_description(cmd_name: str = "") -> str:
        if len(cmd_name):
            return "show help for the command '{}'".format(cmd_name)

        return "show help for commands"

    @staticmethod
    def _help_generic() -> str:
        """show help for commands"""
        result = ("Available commands:\n\n"
                  "exit()\t\texit the script -- also quit()."
                  "help(command)\t\tshows help for the command")

        return result

    @staticmethod
    def _help_command(cmd_name: str) -> str:
        """show help for the command"""
        command = dict_cmd.get_command(cmd_name)
        if command is None:
            raise ValueError("command is None!")

        param = command.get_argument()

        if param is not None:
            help_str = "{}({})\t\t{}".format(command.get_name(), param.name, command.get_description(param.name))
            if not param.required:
                help_str += "\nor\n"
                help_str += "{}()\t\t\t{}".format(command.get_name(), command.get_description())

        else:
            help_str = "{}()\t\t{}".format(command.get_name(), command.get_description())

        if len(command.get_alias()):
            help_str += " -- also {}().".format(command.get_alias())

        return help_str

    @staticmethod
    def execute(cmd_name: str = "") -> str:
        """show help for the command"""
        if len(cmd_name):
            return HelpCommand._help_command(cmd_name)
        else:
            return HelpCommand._help_generic()


dict_cmd.CMD_CLASSES.append(HelpCommand)
