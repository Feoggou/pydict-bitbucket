#!/usr/bin/python3

import sys
import json
import http
from http import client
from threading import Timer
import os
from gi.repository import Notify

sys.path.append("/home/zenith/PycharmProjects/EDictionary/v2")

from src import config

HTML_ALLWORDS_PATH = "/home/zenith/PycharmProjects/EDictionary/v2/html_permanent/all_words.json"
WORDS_RETRIEVED = 0
ALL_ITEMS = []

with open(HTML_ALLWORDS_PATH, "r", encoding="utf-8") as f:
    ALL_ITEMS = json.load(f)


def show_initial_notification():
    global ALL_ITEMS
    Notify.init("WebWordFetcher")

    done = [x for x in ALL_ITEMS if x["have"] is True]
    content = "{} / {}".format(len(done), len(ALL_ITEMS))

    notif_obj = Notify.Notification.new("WebWordFetcher", content, "dialog-information")
    notif_obj.show()


def get_rand_range(maximum):
    value = int().from_bytes(os.urandom(4), byteorder="little")
    value = abs(value)
    value %= maximum
    return value


def get_random_item(to_download: list):
    count = len(to_download)
    index = get_rand_range(count)
    return index


def download_word(item: dict):
    conn = http.client.HTTPConnection(config.HOSTNAME)
    print('getting item: "{}" ({})'.format(item["title"], item["link"]))
    # conn.request("GET", item["link"])
    # reason = conn.getresponse()

    # data = reason.read()
    # html_content = data.decode()


def save_json():
    global HTML_ALLWORDS_PATH, ALL_ITEMS

    with open(HTML_ALLWORDS_PATH, "w", encoding="utf-8") as f:
        json.dump(ALL_ITEMS, f, indent=4, sort_keys=True, ensure_ascii=False)


def timer_callback():
    global HTML_ALLWORDS_PATH, WORDS_RETRIEVED, ALL_ITEMS

    to_download = [x for x in ALL_ITEMS if x["have"] is False]
    print("TODO: {} / {} ".format(len(to_download), len(ALL_ITEMS)))

    index = get_random_item(to_download)
    download_word(to_download[index])

    # NOTE: also writes in all_items
    to_download[index]["have"] = True
    WORDS_RETRIEVED += 1

    if WORDS_RETRIEVED > 10:
        # save_json()
        WORDS_RETRIEVED = 0
        exit(0)

    # timer = Timer(5, timer_callback)
    # timer.start()

show_initial_notification()

timer = Timer(0, timer_callback)
timer.start()
