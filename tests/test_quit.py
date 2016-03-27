import unittest

from src import commands


class TestCommandQuit(unittest.TestCase):
    def test_command_quit_returns_quit_class(self):
        input_str = "quit"

        cmd = commands.get_command(input_str)
        self.assertIsInstance(cmd, commands.QuitCommand)

    def test_command_exit_returns_quit_class(self):
        input_str = "exit"

        cmd = commands.get_command(input_str)
        self.assertIsInstance(cmd, commands.QuitCommand)

    def test_command_quit_exits(self):
        cmd = commands.QuitCommand()

        with self.assertRaises(SystemExit):
            cmd.execute()

    def test_command_quit_has_description(self):
        cmd = commands.QuitCommand()

        description = cmd.get_description()
        self.assertEqual(description, "exit the script")

    def test_command_quit_has_name(self):
        cmd = commands.QuitCommand()

        name = cmd.get_name()
        self.assertEqual(name, "quit")

    def test_command_quit_has_alias(self):
        cmd = commands.QuitCommand()

        alias = cmd.get_alias()
        self.assertEqual(alias, "exit")


if __name__ == '__main__':
    unittest.main()