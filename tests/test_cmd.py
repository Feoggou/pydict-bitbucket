import unittest
from src import commands


class TestCommandQuit(unittest.TestCase):
    def test_match_input_zero_args(self):
        input_str = "quit()"

        cmd = commands.match_command(input_str)

        self.assertEqual("quit", cmd.get_name())
        self.assertEqual(None, cmd.get_argument_value())

    def test_match_input_opt_zero_args(self):
        input_str = "help()"

        cmd = commands.match_command(input_str)

        self.assertEqual("help", cmd.get_name())
        self.assertEqual(None, cmd.get_argument_value())

    def test_match_input_with_arg(self):
        input_str = "help(exit)"

        cmd = commands.match_command(input_str)

        self.assertEqual("help", cmd.get_name())
        self.assertEqual("exit", cmd.get_argument_value())

    def test_command_that_takes_no_argument_when_argument_is_provided_raises_ValueError(self):
        input_str = "quit(exit)"

        with self.assertRaises(ValueError):
            cmd = commands.match_command(input_str)

    def test_default_command_finds_default(self):
        input_str = "do"

        default_cmd = commands.match_command(input_str)
        self.assertIsInstance(default_cmd, commands.DefaultCommand)


if __name__ == "__main__":
    unittest.main()