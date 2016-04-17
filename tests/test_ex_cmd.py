import unittest
from unittest.mock import patch

from src import commands
from src.cmd_ex import ExCommand
from src.colors import *
from src.json_seeker import *


class TestExCommand(unittest.TestCase):
    def setUp(self):
        self.dir_path = "./search-tests-data"

    def test_command_defs_returns_ExCmd_class(self):
        input_str = "ex(do)"

        command = commands.match_command(input_str)
        self.assertIsInstance(command, ExCommand)

    def test_find_play_inDirectory(self):
        cmd = ExCommand("do")
        cmd.set_dir_path(self.dir_path)

        # must: 1. search the directory for all files.
        #       2. retrieve the path to each file.
        #       3. for each file, do a search content on the json file.
        #       4. retrieve content for each file.
        #       5. process content: sorted, unique
        #       6. output process: an object that can be __str__-ed.

        results = cmd.execute().items

        self.assertEqual(results, [
            {
                'do.json': [
                    'what does he do for a living?',
                    'to do honor to the dead',
                    'to do a mile in four minutes',
                    'to do a Houdini',
                    'to do Horace into English',
                    'to do 60 miles an hour',
                    'this will do me very well',
                    'the black dress will do',
                    'love me as I do (love) you',
                    "let's do lunch",
                    "let's do Mexican tonight",
                    'dog do',
                    "do; don't merely talk",
                    'do your best',
                    'do what I tell you',
                    "do the ironing, do one's nails or hair",
                    'do stay a while, do hereby enjoin',
                    'do not go, they do not like it',
                    'do great deeds',
                    'do a problem',
                    '[transl.] When you do something, you take some action or perform an activity or task.I was trying '
                    'to do some work. done'
                ]
            },
            {
                'perform.json': [
                    '[transl.] When you perform a task or action, you do it....people who have performed outstanding '
                    'acts of bravery. performs, performing, performed'
                ]
            }
        ])


if __name__ == '__main__':
    unittest.main()
