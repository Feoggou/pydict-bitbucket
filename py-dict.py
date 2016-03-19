#!/usr/bin/python3

# given "word_name" and "dir_path", must:
# * check that path exists
# * download & parse content
# * create file
# * write to file as json

import sys
import os
import json
import re

from json_printer import JsonPrinter
from word import WordData

dir_path = sys.argv[1]


def get_word_def(word_name):
    word_data = WordData(word_name)
    word_data.fetch()

    content = word_data.build_content()
    file_name = word_name.replace(" ", "-")
    file_name += ".json"
    file_name = os.path.join(dir_path, file_name)

    with open(file_name, "w") as f:
        json.dump(content, f, indent=4, sort_keys=True)

    print("Done! Created file: ", file_name)


def call_printer(word):
    json_printer = JsonPrinter()
    file_name = dir_path + "/" + word + ".json"
    text = json_printer.to_text(file_name)
    print(text)


def call_addex(word):
    json_file_name = dir_path + "/" + word + ".json"

    with open(json_file_name, "r") as json_file:
        obj = json.load(json_file)

    example_value = input("example: ")
    obj["examples"].append({"example": example_value})

    with open(json_file_name, "w") as json_file:
        json.dump(obj, json_file, indent=4, sort_keys=True)


def print_help():
    print("usage:\tpy-dict.py <dir_path> [<word_def>]")


if len(sys.argv) == 1:
    print_help()
    exit(0)

if not os.path.isdir(dir_path):
    print("argument is not a valid directory path: ", dir_path)
    exit(-1)

if len(sys.argv) > 2:
    word_name = sys.argv[2]
    get_word_def(word_name)
    exit(0)


word_name = ""

while True:
    word_name = input("command: ")
    assert isinstance(word_name, str)

    if word_name == "quit()" or word_name == "exit()":
        exit()

    elif word_name == "search()":
        print("search not yet implemented!")

    elif re.match("^addex\(.*\)$", word_name):
        value = re.match("addex\((\w+)\)", word_name)
        if value is not None:
            call_addex(value.groups()[0])
        else:
            print("word not found!")

    elif re.match("^print\(.*\)$", word_name):
        value = re.match("print\((\w+)\)", word_name)
        if value is not None:
            call_printer(value.groups()[0])
        else:
            print("no word to print!")

    elif re.match("^[A-Za-z\-0-9]+$", word_name):
        if os.path.exists(dir_path + "/" + word_name + ".json"):
            x = input("The json file exists, do you want to replace it? (Yes/No)\n")
            assert(isinstance(x, str))
            if x.upper() != "YES":
                continue

        get_word_def(word_name)
        # TODO: get word def ONLY IF not found. Also print the read result.

    else:
        print("Error: unrecognized command, nor word.")


print("Bye!\n")

