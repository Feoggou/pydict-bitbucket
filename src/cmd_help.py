from . import commands
from .dict_cmd import Command, Parameter


class HelpCommand(Command):
    def __init__(self, arg: str = None):
        Command.__init__(self)

        self._argument = arg
        if arg == "":
            raise ValueError("Help command: Unexpected argument: ''")

    @staticmethod
    def get_name() -> str:
        return "help"

    @staticmethod
    def get_alias() -> str:
        return ""

    @staticmethod
    def get_argument_info() -> Parameter:
        return Parameter("cmd", required=False)

    def set_argument_value(self, v: str):
        self._argument = v

    def get_argument_value(self) -> str:
        return self._argument

    @staticmethod
    def get_description(cmd_name: str = "") -> str:
        if len(cmd_name):
            return "show help for the command '{}'".format(cmd_name)

        return "show help for commands"

    @staticmethod
    def _build_help_simple(cmd_class: Command) -> str:
        help_str = "{:14}{}".format(cmd_class.get_name() + "()", cmd_class.get_description())
        return help_str

    @staticmethod
    def _build_help_with_param(cmd_class: Command, param: Parameter) -> str:
        cmd_call = "{}({})".format(cmd_class.get_name(), param.name)
        help_str = "{:14}{}".format(cmd_call, cmd_class.get_description(param.name))
        return help_str

    @staticmethod
    def _help_generic() -> str:
        """show help for commands"""
        result = "Available commands:\n\n"
        result += HelpCommand._build_help_simple(HelpCommand) + "\n"

        for command in commands.CMD_CLASSES:
            if command is not HelpCommand:
                result += HelpCommand._help_command(command.get_name()) + "\n"

        return result

    @staticmethod
    def _help_command(cmd_name: str) -> str:
        """show help for the command"""
        command = commands.get_command(cmd_name)
        if command is None:
            raise ValueError("command is None!")

        param = command.get_argument_info()

        if param is not None:
            help_str = HelpCommand._build_help_with_param(command, param)
            if not param.required:
                help_str += "\nor\n"
                help_str += HelpCommand._build_help_simple(command)

        else:
            help_str = HelpCommand._build_help_simple(command)

        if len(command.get_alias()):
            help_str += " -- also {}()".format(command.get_alias())

        return help_str

    def execute(self) -> str:
        if self._argument is not None and len(self._argument):
            return HelpCommand._help_command(self._argument)
        else:
            return HelpCommand._help_generic()


commands.CMD_CLASSES.append(HelpCommand)
