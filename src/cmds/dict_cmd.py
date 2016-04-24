

class Parameter:
    def __init__(self, name: str, required: bool):
        self.name = name
        self.required = required
        self.value = None


class Command:
    def __init__(self):
        self.dir_path = ""

    @staticmethod
    def get_name() -> str:
        raise NotImplementedError()

    @staticmethod
    def get_alias() -> str:
        raise NotImplementedError()

    @staticmethod
    def get_description(cmd_name: str = "") -> str:
        raise NotImplementedError()

    # TODO: get_argument_info is used only in help. I don't think it's very useful.
    @staticmethod
    def get_argument_info() -> Parameter:
        raise NotImplementedError()

    def get_argument_value(self) -> str:
        raise NotImplementedError()

    def set_dir_path(self, dir_path: str):
        self.dir_path = dir_path

    def execute(self) -> str:
        raise NotImplementedError()


CMD_CLASSES = []
