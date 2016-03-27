#!/usr/bin/python3

import sys
import os
from src.dict_cmd import *
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
    word_name = input(BOLDBLACK + "Dict> " + RESET)

    print(word_name)

