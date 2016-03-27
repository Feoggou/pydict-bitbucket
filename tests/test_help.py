import unittest

from src import commands


class TestCommandHelp(unittest.TestCase):
    def test_command_help_returns_help_class(self):
        input_str = "help"

        cmd = commands.get_command(input_str)
        self.assertIsInstance(cmd, commands.HelpCommand)

    def test_command_help_has_name(self):
        cmd = commands.HelpCommand()

        name = cmd.get_name()
        self.assertEqual(name, "help")

    def test_command_help_has_no_alias(self):
        cmd = commands.HelpCommand()

        alias = cmd.get_alias()
        self.assertEqual(alias, "")

    def test_command_help_has_description(self):
        cmd = commands.HelpCommand()

        description = cmd.get_description()
        self.assertEqual(description, "show help for commands")

    def test_command_help_on_quit(self):
        cmd = commands.HelpCommand()

        # Dict> help(quit)
        result = cmd.execute("quit")

        self.assertEqual("quit()\t\texit the script -- also exit().", result)

    def test_command_help_on_exit(self):
        cmd = commands.HelpCommand()

        # Dict> help(exit)
        result = cmd.execute("exit")

        self.assertEqual(result, "quit()\t\texit the script -- also exit().")

    def test_command_help_on_help(self):
        cmd = commands.HelpCommand()

        # Dict> help(help)
        result = cmd.execute("help")

        print(result)

        self.assertEqual("help(cmd)\t\tshow help for the command 'cmd'\n"
                         "or\n"
                         "help()\t\t\tshow help for commands",
                         result)

    def test_command_help_with_no_param_shows_all(self):
        cmd = commands.HelpCommand()

        result = cmd.execute()

        self.assertEqual(result,
            "Available commands:\n\n"
            "exit()\t\texit the script -- also quit()."
            "help(command)\t\tshows help for the command")

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