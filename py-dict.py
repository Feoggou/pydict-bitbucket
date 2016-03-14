#!/usr/bin/python3

# given "word_name" and "dir_path", must:
# * check that path exists
# * download & parse content
# * create file
# * write to file as json

import sys
import os
import json

from word import WordData


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


dir_path = sys.argv[1]
if not os.path.isdir(dir_path):
    print("argument is not a valid directory path: ", dir_path)
    exit(-1)

if len(sys.argv) > 2:
    word_name = sys.argv[2]
    get_word_def(word_name)
    exit(0)


word_name = ""

while True:
    word_name = input("word: ")
    assert isinstance(word_name, str)
    print("word_name = ", word_name)

    if word_name == "quit()" or word_name == "exit()":
        exit()

    get_word_def(word_name)

print("Bye!\n")

