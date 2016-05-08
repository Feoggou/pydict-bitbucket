import re

from .dict_cmd import Command
from .. import word


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

    @staticmethod
    def get_name() -> str:
        return ""

    @staticmethod
    def get_alias() -> str:
        return ""

    def _fetch_content(self, word_name: str):
        word_data = word.WordData(word_name)
        word_data.fetch()

        content = word_data.build_content()
        return content

    def execute(self, word: str) -> dict:
        """Retrieves the content for the word self._word

        Performs the required word validation.
        Returns a dict object containing the word. Either from the web site or offline, depending where it can be found.
        If the word cannot be found (either doesn't exist or the site redirects to a different location), the
        appropriate exception is risen.
        """

        if word is None:
            raise WordInvalidError("No word was provided!")

        match = re.match("^[\w\- \.\']+$", word)

        if match is None:
            raise WordInvalidError(word)

        word_u8 = word.replace(" ", "-")

        content = self._fetch_content(word_u8)
        return content

