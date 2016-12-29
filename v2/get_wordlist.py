#!/usr/bin/python3

import sys

import http
import string
import time
import json
import os
from http import client
from lxml import etree

sys.path.append("/home/zenith/PycharmProjects/py-dict/v2")

from src import config

conn = http.client.HTTPConnection(config.HOSTNAME)
base_http_path = "/browse/english/words-starting-with-"

ALL_JSON_ITEMS = []
HTML_BASE = "/home/zenith/PycharmProjects/py-dict/v2/html_permanent"
DOTS = int(0)


def HTML_PLUS(letter: str):
    return os.path.join(HTML_BASE, letter + "-plus.json")


def HTML_MINUS(letter: str):
    return os.path.join(HTML_BASE, letter + "-minus.json")


def get_sublist(sublist: etree._Element):
    global DOTS
    http_path = sublist.get("href")

    while True:
        try:
            conn.request("GET", http_path)
            break
        except:
            print("sublist error...")
            time.sleep(20)

    reason = conn.getresponse()

    data = reason.read()
    html_content = data.decode()

    root = etree.HTML(html_content)
    items = root.xpath('.//main/div[@class="browse_wrapper"]/div[@class="res_cell_center"]//'
                       'ul[@class="columns2 browse-list"]/li/a')

    print("{} items{}".format(len(items), DOTS * "."))
    DOTS = (DOTS + 1) % 4

    result_items = []

    for item in items:
        title = item.get("title")
        link = item.get("href")
        json_obj = {"title": title, "link": link, "have": False}
        result_items.append(json_obj)
        # break  # TODO

    return result_items

ALL_LETTERS = 'wxyz'

for letter in ALL_LETTERS:
    http_path = base_http_path + letter
    print("LETTER: {}\n".format(letter))

    while True:
        try:
            conn.request("GET", http_path)
            break
        except:
            print("letter error...")
            time.sleep(20)

    reason = conn.getresponse()

    data = reason.read()
    html_content = data.decode()

    root = etree.HTML(html_content)
    sublists = root.xpath('.//main/div[@class="browse_wrapper"]/div[@class="res_cell_center"]//'
                          'ul[@class="columns2 browse-list"]/li/a')

    print("Found {} lists or letter '{}'!".format(len(sublists), letter))

    letter_items = []
    for sublist in sublists:
        items = get_sublist(sublist)
        letter_items += items

        # break  # TODO

    existing_file = os.path.join(HTML_BASE, letter + ".json")

    with open(existing_file, "r", encoding="utf-8") as f:
        existing_items = json.load(f)

    existing_links = [x["link"] for x in existing_items]
    now_links = [x["link"] for x in letter_items]

    plus_links = set(now_links) - set(existing_links)
    minus_links = set(existing_links) - set(now_links)

    print("PLUS ITEMS: {}; MINUS ITEMS: {} [existing={}; now={}]".format(len(plus_links), len(minus_links),
          len(existing_items), len(letter_items)))

    plus_items = [x for x in letter_items if x["link"] in plus_links]
    minus_items = [x for x in existing_items if x["link"] in minus_links]

    with open(HTML_PLUS(letter), "w", encoding="utf-8") as f:
        json.dump(plus_items, f, indent=4, sort_keys=True, ensure_ascii=False)

    with open(HTML_MINUS(letter), "w", encoding="utf-8") as f:
        json.dump(minus_items, f, indent=4, sort_keys=True, ensure_ascii=False)

    print("\n\n")
