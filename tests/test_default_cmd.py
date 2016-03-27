import unittest

from src import commands
from src.cmd_default import DefaultCommand


class TestCommandHelp(unittest.TestCase):
    def test_command_default_returns_Default_class(self):
        input_str = "do"

        command = commands.match_command(input_str)
        self.assertIsInstance(command, DefaultCommand)
        self.assertEqual("do", command.get_argument_value())


if __name__ == '__main__':
    unittest.main()
