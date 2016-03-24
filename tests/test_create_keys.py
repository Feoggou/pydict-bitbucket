#!/usr/bin/python3.5

import http.client
from lxml import etree
from src.etree_printer import *
import sys


def get_html_for_word(word):
    text = ""
    if 1:
        hostname = "www.collinsdictionary.com"
        conn = http.client.HTTPConnection(hostname)
        conn.request("GET", "/dictionary/american/" + word)
        response = conn.getresponse()
        loc = response.getheader('location')
        if loc is not None:
            print("loc = ", loc)

        data = response.read()
        text = data.decode()
    else:
        f = open("old_do_defs.htm")
        text = f.read()
    return text


def get_def_new(word):
    f = open("do_defs.html")
    text = f.read()
    return text

def get_related_for_word(word):
    text = ""
    # f = open("file.htm")
    f = open("do_related.html")
    text = f.read()
    return text


def get_syn_for_word(word):
    text = ""
    # f = open("file.htm")
    f = open("do_syn.html")
    text = f.read()
    return text


add_new_word_to_test = True
word_name = "bellow"

if add_new_word_to_test is True:
    text = get_html_for_word(word_name)
    with open(word_name + "_defs.html", "w") as f:
        f.write(text)

    root = etree.HTML(text)

    temp = sys.stdout
    sys.stdout = open(word_name + "_defs.keys.txt", "w")
    print_children(root, padding=0)
    sys.stdout = temp
else:
    # text = get_related_for_word("do")
    # text = get_syn_for_word("do")
    text = get_def_new("do")

# traverse_children(root, None)
