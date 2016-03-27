from .dict_cmd import Command


class DefaultCommand(Command):
    def __init__(self):
        self._argument = None

    @staticmethod
    def get_name() -> str:
        return ""

    @staticmethod
    def get_alias() -> str:
        return ""

    def set_argument_value(self, v: str):
        self._argument = v

    def get_argument_value(self) -> str:
        return self._argument
