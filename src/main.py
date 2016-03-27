#!/usr/bin/python3

import sys
import os
from src import commands
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


while True:
    input_str = input(BOLDBLACK + "Dict> " + RESET)

    cmd = commands.match_command(input_str)
    print(cmd.execute())


