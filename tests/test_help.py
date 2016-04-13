import unittest

from src import commands
from src.cmd_help import HelpCommand


class TestCommandHelp(unittest.TestCase):
    def test_command_help_returns_help_class(self):
        input_str = "help"

        command = commands.get_command(input_str)
        self.assertIsInstance(command, HelpCommand)

    def test_command_help_has_name(self):
        command = HelpCommand()

        name = command.get_name()
        self.assertEqual(name, "help")

    def test_command_help_has_no_alias(self):
        command = HelpCommand()

        alias = command.get_alias()
        self.assertEqual(alias, "")

    def test_command_help_has_description(self):
        command = HelpCommand()

        description = command.get_description()
        self.assertEqual(description, "show help for commands")

    def test_command_help_on_quit(self):
        command = HelpCommand()
        command.set_argument_value("quit")

        # Dict> help(quit)
        result = command.execute()

        self.assertEqual("quit()        exit the script -- also exit()", result)

    def test_command_help_on_exit(self):
        command = HelpCommand()
        command.set_argument_value("exit")

        # Dict> help(exit)
        result = command.execute()

        self.assertEqual(result, "quit()        exit the script -- also exit()")

    def test_command_help_on_help(self):
        command = HelpCommand()
        command.set_argument_value("help")

        # Dict> help(help)
        result = command.execute()

        print(result)

        self.assertEqual("help(cmd)     show help for the command 'cmd'\n"
                         "or\n"
                         "help()        show help for commands",
                         result)

    def test_cmd_help_matched_with_argument(self):
        # Dict> help(exit)
        command = commands.match_command("help(exit)")
        result = command.execute()

        self.assertEqual("quit()        exit the script -- also exit()", result)

    def test_cmd_help_matched_no_argument(self):
        # Dict> help(exit)
        command = commands.match_command("help()")
        result = command.execute()

        self.assertIn("Available commands", result)

    def test_command_help_with_no_param_shows_all(self):
        command = HelpCommand()

        result = command.execute()

        self.assertEqual(result,
            "Available commands:\n\n"
            "help()        show help for commands\n"
            "quit()        exit the script -- also exit()\n"
            "print()       print all info from json in textual format\n")

            # "defs(word)\tsearch all .json files, and print all definitions\n"
            #     "\t\tthat contain the word <word>"
            # "ex(word)\tsearch all .json files, and print all examples that\n"
            #     "\t\tcontain the word <word>"
            # "show(word)\tshow the json file for the word"
            # "related(word)\tprint all related words from .json"
            # "nearby(word)\tprint the nearby words from .json"
            # "search(word)\tsearch all .json files for the word (searches contents)"
            # "addex(word)\tadd an example json object into the .json file"
            # "print(word)\tprints a concise .txt representation for the .json file"
            # "word\t\tif the file <word>.json does not exist, downloads the\n"
            #     "\t\tcontent and creates it. Prints the textual representation\n"
            #     "\t\tin either case.\n")


if __name__ == '__main__':
    unittest.main()
