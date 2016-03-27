

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


CMD_CLASSES = []
