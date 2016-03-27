#!/usr/bin/python3

from gi.repository import Notify
from threading import Timer
import sys
import random
import os
import json

sys.path.append("/home/zenith/PycharmProjects/EDictionary")
dict_path = "/home/zenith/Dropbox/Docs/DICTIONARY"

# count_times = 0
random.seed()

Notify.init("EDictionary")


def get_random_word(dir_path: str) -> dict:
    items = os.listdir(dir_path)
    items = [x for x in items if os.path.isfile(os.path.join(dir_path, x))]
    items = [x for x in items if ".json" in x]

    if len(items) == 0:
        return None

    index = random.randrange(0, len(items))
    word = items[index]
    file_name = os.path.join(dir_path, word)

    with open(file_name, "r") as f:
        try:
            dict_obj = json.load(f)
        except:
            show_notification("EDictionary --- " + word, "ERROR: " + str(sys.exc_info()[0]))
            dict_obj = None

    return dict_obj


def read_definition(definition, indent: int = 0) -> str:
    tab = "    "

    if "def_subgroup" in definition.keys():
        s = ""
        if "category" in definition.keys():
            s += "({}) ".format(definition["category"])
        s = "{} {}\n".format(tab * indent, s)
        for subdef in definition["def_subgroup"]:
            s += read_definition(subdef, indent + 1)
    else:
        s = definition["def"]
        if "example" in definition.keys():
            s += "\n{}e.g. {}".format(tab * (indent + 2), definition["example"])
        if "category" in definition.keys():
            s = "({}) {}".format(definition["category"], s)

        s = (tab * indent) + " " + s
        s += "\n"

    return s


def get_random_definition(dict_obj: dict) -> (str, str):
    def_groups = dict_obj["def_groups"]
    index = random.randrange(0, len(def_groups))

    def_group = def_groups[index]
    word = def_group["word"]
    word = "{} ({})".format(word, dict_obj["frequency"])
    ggroups = def_group["gram_groups"]
    index = random.randrange(0, len(ggroups))
    ggroup = ggroups[index]
    defs = ggroup["defs"]
    index = random.randrange(0, len(defs))
    definition = read_definition(defs[index])

    return word, definition


def show_notification(word: str, definition: str):
    notif_obj = Notify.Notification.new(word, definition, "dialog-information")
    notif_obj.show()


def timer_callback():
    dict_obj = get_random_word(dict_path)

    if dict_obj is not None:
        word, definition = get_random_definition(dict_obj)
        show_notification("word:   " + word, definition)

    timer = Timer(20 * 60, timer_callback)
    timer.start()


timer = Timer(2, timer_callback)
timer.start()


