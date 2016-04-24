
import unittest
from unittest.mock import patch
from unittest import mock
import copy

import difflib

from src import colors

A = """[In Common Usage]

DEFINTIONS
affluent
adjective
o) flowing freely
o) plentiful; abundant
o) wealthy; prosperous; rich
    e.g. the affluent society

noun
o) a tributary stream opposed to effluent (def. 1)noun, effluent (sense 2a) (def. 1)
o) an affluent person


TRANSLATIONS
If you are affluent, you have a lot of money.It is one of the most affluent areas in the country.
The affluent are people who are affluent.The diet of the affluent has not changed much over the decades.


SYNONYMS
affluent
adjective
o) (slang informal) wealthy, loaded, moneyed, opulent, prosperous, rich, well-heeled, well-off, well-to-do


EXAMPLES
o) Adam Berendt who'd lived so frugally in the midst of affluent Salthill.

"""

B = """[In Common Usage]

DEFINTIONS
affluent
adjective
o) flowing freely
o) plentiful; abundant
o) wealthy; prosperous; rich
    e.g. the affluent society

noun
o) a tributary stream opposed to effluent (def. 1)noun, effluent (sense 2a) (def. 1)
o) an affluent person
o) an KGJJK person


TRANSLATIONS
If you are affluent, you have a lot of money.It is one of the most affluent areas in the country.
The affluent are people who are affluent.The diet of the affluent has not changed much over the decades.


SYNONYMS
affluent
adjective
o) (slang informal) wealthy, loaded, moneyed, opulent, prosperous, rich, well-heeled, well-off, well-to-do


EXAMPLES
o) Adam Berendt who'd lived so frugally in the midst of affluent Salthill.

"""


class ModifiedMagicMock(mock.MagicMock):
    def _mock_call(_mock_self, *args, **kwargs):
        return super(ModifiedMagicMock, _mock_self)._mock_call(*copy.deepcopy(args), **copy.deepcopy(kwargs))


class MyClass:
    def foo(self):
        items = ["A"]

        self.bar(items)

        items.append("B")

        print(items)

    def bar(self, items):
        pass


class MyTest(unittest.TestCase):
    @patch.object(MyClass, "bar", auto_spec=True)
    @patch("unittest.mock.MagicMock", new=ModifiedMagicMock)
    @unittest.skip("dummy")
    def test_MyClass(self, mock_bar):
        obj = MyClass()

        # with patch("path", new_callable=DeepCopyMock):
        obj.foo()

        mock_bar.assert_called_once_with(["A", "B"])

    @unittest.skip("dummy")
    def test_ndiff(self):
        result = difflib.unified_diff(A.splitlines(), B.splitlines())
        for line in result:
            if line[0] == "+":
                line = colors.GREEN + line + colors.RESET
            elif line[0] == "-":
                line = colors.RED + line + colors.RESET
            elif line.startswith("@@") and line.endswith("@@\n"):
                print("begins with and ends with!")
                line = colors.YELLOW + line + colors.RESET
            print(line)


if __name__ == "__main__":
    unittest.main()
