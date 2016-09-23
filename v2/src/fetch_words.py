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

# a, b, c, d, p, m, t, l, f, r, g
LETTER = "h"

HTML_ALLWORDS_PATH = "/home/zenith/PycharmProjects/EDictionary/v2/html_permanent/{}.json".format(LETTER)
HTML_PERMANENT_PATH = "/home/zenith/PycharmProjects/EDictionary/v2/html_permanent/html"
WORDS_RETRIEVED = 0
ALL_ITEMS = []
FAILED_ITEMS = []

with open(HTML_ALLWORDS_PATH, "r", encoding="utf-8") as f:
    ALL_ITEMS = json.load(f)


def show_initial_notification():
    global ALL_ITEMS, LETTER
    Notify.init("WebWordFetcher")

    done = [x for x in ALL_ITEMS if x["have"] is True]
    content = "{}: {} / {}".format(LETTER, len(done), len(ALL_ITEMS))

    notif_obj = Notify.Notification.new("WebWordFetcher", content, "dialog-information")
    notif_obj.show()


def show_notif_error(error_msg: str):
    notif_obj = Notify.Notification.new("WebWordFetcher", error_msg, "dialog-error")
    notif_obj.show()


def get_rand_range(maximum):
    value = int().from_bytes(os.urandom(4), byteorder="little")
    value = abs(value)
    value %= maximum
    return value


def get_random_item(to_download: list):
    count = len(to_download)
    if count == 0:
        return -1
    index = get_rand_range(count)
    return index


def download_html(word: str, http_path, file_suffix: str):
    conn = http.client.HTTPConnection(config.HOSTNAME)

    conn.request("GET", http_path + word)
    reason = conn.getresponse()

    data = reason.read()
    html_content = data.decode()

    if len(html_content) == 0:
        print("{} --- could not be downloaded.".format(word + file_suffix))
        return False

    file_name = os.path.join(HTML_PERMANENT_PATH, word + file_suffix)

    with open(file_name, "w") as f:
        f.write(html_content)

    return True


def download_word(item: dict):
    print('downloading... "{}" ({})'.format(item["title"], item["link"]))
    word = item["link"].split('/')[-1]

    ret = download_html(word, config.HTTP_PATH, "_defs.html")
    download_html(word, config.SYN_HTTP_PATH, "_syn.html")

    return ret


def save_json():
    global HTML_ALLWORDS_PATH, ALL_ITEMS

    with open(HTML_ALLWORDS_PATH, "w", encoding="utf-8") as f:
        json.dump(ALL_ITEMS, f, indent=4, sort_keys=True, ensure_ascii=False)


def timer_callback():
    global HTML_ALLWORDS_PATH, WORDS_RETRIEVED, ALL_ITEMS, TIMER, FAILED_ITEMS

    to_download = [x for x in ALL_ITEMS if x["have"] is False and x not in FAILED_ITEMS]
    print("TODO: {} / {} ".format(len(to_download), len(ALL_ITEMS)))

    index = get_random_item(to_download)
    if index == -1:
        save_json()
        Notify.Notification.new("WebWordFetcher", "Finished!", "dialog-warning")
        print("ITEMS THAT FAILED:\n", FAILED_ITEMS)
        exit(0)

    if download_word(to_download[index]) is True:
        # NOTE: also writes in all_items
        to_download[index]["have"] = True
        WORDS_RETRIEVED += 1

        if WORDS_RETRIEVED >= 10:
            save_json()
            WORDS_RETRIEVED = 0
    else:
        show_notif_error("ERROR: Could not download: " + to_download[index]["link"])
        FAILED_ITEMS.append(to_download[index])

    mseconds = get_rand_range(7000)
    seconds = 1 + float(mseconds) / 1000.0
    print("next: ", seconds, "[{}]".format(WORDS_RETRIEVED))
    TIMER = Timer(seconds, timer_callback)
    TIMER.start()

show_initial_notification()

TIMER = Timer(0, timer_callback)
TIMER.start()
