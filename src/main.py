#!/usr/bin/python3

import sys
import os

sys.path.append("/home/zenith/PycharmProjects/EDictionary")

from src import commands
from src.cmd_getword import GetWordCommand
from src.word_handler import WordHandler
from src.colors import *

DIR_PATH = ""

if "/home/zenith/PycharmProjects/EDictionary/src" == os.getcwd():
    DIR_PATH = "/home/zenith/PycharmProjects/EDictionary/temp-data"
else:
    DIR_PATH = "/home/zenith/Dropbox/Docs/DICTIONARY"

print("DIR_PATH: ", DIR_PATH)

if len(sys.argv) == 2:
    print("NOT IMPLEMENTED YET!")
    exit(0)
elif len(sys.argv) > 2:
    print("UNEXPECTED ARGUMENTS!")
    exit(-1)

os.makedirs(DIR_PATH, exist_ok=True)

while True:
    input_str = input(BOLDMAGENTA + "Dict> " + RESET)

    cmd = commands.match_command(input_str, DIR_PATH)
    if isinstance(cmd, GetWordCommand):
        word_handler = WordHandler(DIR_PATH)
        word_handler.get(input_str)
    else:
        print(cmd.execute())


