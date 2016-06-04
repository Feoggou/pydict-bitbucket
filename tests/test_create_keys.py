#!/usr/bin/python3.5

import http.client
from lxml import etree
from src.html_parser.etree_printer import *
import sys


def get_html_for_word(word):
    text = ""
    if 1:
        hostname = "www.collinsdictionary.com"
        conn = http.client.HTTPConnection(hostname)
        conn.request("GET", "/dictionary/english/" + word)
        # http://www.collinsdictionary.com/dictionary/english/do
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


def get_related_for_word(word):
    text = ""
    hostname = "www.collinsdictionary.com"
    conn = http.client.HTTPConnection(hostname)
    conn.request("GET", "/dictionary/english/" + word + "/related")
    response = conn.getresponse()
    loc = response.getheader('location')
    if loc is not None:
        print("loc = ", loc)

    data = response.read()
    text = data.decode()
    return text


def get_syn_for_word(word):
    text = ""
    hostname = "www.collinsdictionary.com"
    conn = http.client.HTTPConnection(hostname)
    conn.request("GET", "/dictionary/english-thesaurus/" + word)
    # http://www.collinsdictionary.com/dictionary/english-thesaurus/do
    response = conn.getresponse()
    loc = response.getheader('location')
    if loc is not None:
        print("loc = ", loc)

    data = response.read()
    text = data.decode()
    return text


add_new_word_to_test = True
word_name = "do"

if add_new_word_to_test is True:
    text_def = get_html_for_word(word_name)
    with open(word_name + "_defs.html", "w") as f:
        f.write(text_def)

    # text_related = get_related_for_word(word_name)
    # with open(word_name + "_related.html", "w") as f:
    #     f.write(text_related)

    text_syn = get_syn_for_word(word_name)
    with open(word_name + "_syn.html", "w") as f:
        f.write(text_syn)

    assert len(text_def)
    root = etree.HTML(text_def)

    temp = sys.stdout
    sys.stdout = open(word_name + "_defs.keys.txt", "w")
    print_children(root, padding=0)

    """if len(text_related):
        root = etree.HTML(text_related)
        sys.stdout = open(word_name + "_related.keys.txt", "w")
        print_children(root, padding=0)"""

    if len(text_syn):
        root = etree.HTML(text_syn)
        sys.stdout = open(word_name + "_syn.keys.txt", "w")
        print_children(root, padding=0)

    sys.stdout = temp
else:
    # text = get_related_for_word("do")
    # text = get_syn_for_word("do")
    pass

# traverse_children(root, None)
