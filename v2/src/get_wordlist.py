#!/usr/bin/python3

import sys

import http
import string
import json
from http import client
from lxml import etree

sys.path.append("/home/zenith/PycharmProjects/EDictionary/v2")

from src import config

conn = http.client.HTTPConnection(config.HOSTNAME)
base_http_path = "/browse/english/words-starting-with-"

ALL_JSON_ITEMS = []
HTML_ALLWORDS_PATH = "/home/zenith/PycharmProjects/EDictionary/v2/html_permanent/all_words.json"
DOTS = int(0)


def get_sublist(sublist: etree._Element):
    global DOTS
    http_path = sublist.get("href")

    conn.request("GET", http_path)
    reason = conn.getresponse()

    data = reason.read()
    html_content = data.decode()

    root = etree.HTML(html_content)
    items = root.xpath('.//main/div[@class="browse_wrapper"]/div[@class="res_cell_center"]//'
                       'ul[@class="columns2 browse-list"]/li/a')

    print("{} items{}".format(len(items), DOTS * "."))
    DOTS = (DOTS + 1) % 4

    for item in items:
        title = item.get("title")
        link = item.get("href")
        json_obj = {"title": title, "link": link, "have": False}
        ALL_JSON_ITEMS.append(json_obj)


for letter in string.ascii_lowercase:
    http_path = base_http_path + letter
    print("LETTER: {}\n".format(letter))

    conn.request("GET", http_path)
    reason = conn.getresponse()

    data = reason.read()
    html_content = data.decode()

    root = etree.HTML(html_content)
    sublists = root.xpath('.//main/div[@class="browse_wrapper"]/div[@class="res_cell_center"]//'
                          'ul[@class="columns2 browse-list"]/li/a')

    print("Found {} lists or letter '{}'!".format(len(sublists), letter))

    for sublist in sublists:
        get_sublist(sublist)

    print("\n\n")

with open(HTML_ALLWORDS_PATH, "w", encoding="utf-8") as f:
    json.dump(ALL_JSON_ITEMS, f, indent=4, sort_keys=True, ensure_ascii=False)
