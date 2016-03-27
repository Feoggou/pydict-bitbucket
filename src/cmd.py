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
        command = get_command(cmd_name)
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


def get_command(in_str: str) -> Command:
    if in_str == QuitCommand.get_name() or in_str == QuitCommand.get_alias():
        return QuitCommand()

    if in_str == HelpCommand.get_name():
        return HelpCommand()
