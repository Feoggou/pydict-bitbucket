#!/usr/bin/python3

import sys
import os

sys.path.append("/home/zenith/PycharmProjects/EDictionary")

from src.cmds import commands
from src.cmds.cmd_getword import GetWordCommand
from src.cmds.word_handler import WordHandler
from src.colors import *

DIR_PATH = ""

if "/home/zenith/PycharmProjects/EDictionary/src" == os.getcwd():
    DIR_PATH = "/home/zenith/PycharmProjects/EDictionary/temp-data"
    # DIR_PATH = "/home/zenith/dictionary/words"
else:
    DIR_PATH = "/home/zenith/Dropbox/Docs/DICTIONARY"

print("DIR_PATH: ", DIR_PATH)


def execute_command(input_str):
    try:
        cmd = commands.match_command(input_str, DIR_PATH)
    except ValueError as e:
        print(e)
    else:
        if isinstance(cmd, GetWordCommand):
            word_handler = WordHandler(DIR_PATH)
            word_handler.get(input_str)
        else:
            try:
                print(cmd.execute())
            except FileNotFoundError as e:
                item = os.path.split(e.filename)[-1]
                print("File not found: ", item)


if len(sys.argv) == 2:
    input_str = sys.argv[1]
    execute_command(input_str)
    exit(0)
elif len(sys.argv) > 2:
    print("UNEXPECTED ARGUMENTS!")
    exit(-1)

os.makedirs(DIR_PATH, exist_ok=True)


while True:
    input_str = input(BOLDMAGENTA + "Dict> " + RESET)
    if len(input_str) == 0:
        continue

    execute_command(input_str)


