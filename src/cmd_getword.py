import re

from .dict_cmd import Command
from . import word


class WordInvalidError(RuntimeError):
    def __init__(self, value):
        self.msg = value

    def __str__(self):
        return "Invalid word: " + self.msg


class GetWordCommand(Command):
    """Responsible with taking the content of the word as json / dict object"""
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
        """Retrieves the content for the word self._word

        Performs the required word validation.
        Returns a dict object containing the word. Either from the web site or offline, depending where it can be found.
        If the word cannot be found (either doesn't exist or the site redirects to a different location), the
        appropriate exception is risen.
        """

        if self._word is None:
            raise WordInvalidError("No word was provided!")

        match = re.match("^[A-Za-z0-9\- \.\']+$", self._word)

        if match is None:
            raise WordInvalidError(self._word)

        self._word = self._word.replace(" ", "-")

        """# TODO: Not actually part of 'getword' responsibility
        content = None

        # TODO: Redirection not actually part of 'getword' responsibility
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

        # if word is 'doing', and contains wordform 'do', then ask user.
        # if 'do' exists, we must read do and make sure it is the same. if so, do not take that defgroup. else, take it.
        # if 'do' doesn't exist, we must ask user if he wants to take it separately. (auto=separate)"""

        content = self._fetch_content()

        return content

