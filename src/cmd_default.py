import re

from .dict_cmd import Command
from . import word


class WordInvalidError(RuntimeError):
    def __init__(self, value):
        self.msg = value

    def __str__(self):
        return "Invalid word: " + self.msg


class DefaultCommand(Command):
    def __init__(self, auto=False):
        Command.__init__(self)
        self.auto = auto
        self._word = None

    @staticmethod
    def get_name() -> str:
        return ""

    @staticmethod
    def get_alias() -> str:
        return ""

    def set_argument_value(self, v: str):
        self._word = v

    def get_argument_value(self) -> str:
        return self._word

    def _word_already_exists(self) -> bool:
        raise NotImplementedError

    def _call_printer(self):
        raise NotImplementedError

    def _redirect_to(self, url: str) -> dict:
        raise NotImplementedError

    def _ask_redirect(self, url: str):
        question = "Word '{}' not found. Redirect to '{}'? (Yes/No) ".format(self._word, url)
        answer = input(question)
        if answer.lower() == "yes":
            return True
        else:
            return False

    def _fetch_content(self):
        word_data = word.WordData(self._word)
        word_data.fetch()

        content = word_data.build_content()
        return content

    def execute(self) -> dict:
        match = re.match("^[A-Za-z0-9\- \.\']+$", self._word)
        if match is None:
            raise WordInvalidError(self._word)

        self._word = self._word.replace(" ", "-")

        if self._word_already_exists():
            self._call_printer()
            return None

        content = None

        try:
            content = self._fetch_content()
        except word.RedirectError as e:
            if self.auto:
                return self._redirect_to(e.value)
            else:
                redirect = self._ask_redirect(e.value)
                if redirect is True:
                    return self._redirect_to(e.value)
                return None


        return content

