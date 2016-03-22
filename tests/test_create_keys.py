#!/usr/bin/python3.5

import http.client
from lxml import etree
from src.etree_printer import *


def get_html_for_word(word):
    text = ""
    if 1:
        hostname = "www.collinsdictionary.com"
        conn = http.client.HTTPConnection(hostname)
        conn.request("GET", "/dictionary/american/" + word)
        reason = conn.getresponse()
        data = reason.read()
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


# text = get_html_for_word("perform")
# text = get_related_for_word("do")
# text = get_syn_for_word("do")
text = get_def_new("do")

# with open("perform_defs.html", "w") as f:
#     f.write(text)

root = etree.HTML(text)

# temp = sys.stdout
# sys.stdout = open("perform_defs.keys.txt", "w")
print_children(root, padding=0)
# sys.stdout = temp

# traverse_children(root, None)
