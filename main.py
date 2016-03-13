#!/usr/bin/python3.5

import http.client
from lxml import etree
from etree_printer import *
# from lxml.html import tostring, fromstring
# from html_parse import traverse_children


def get_html_for_word(word):
    text = ""
    if 0:
        hostname = "www.collinsdictionary.com"
        conn = http.client.HTTPConnection(hostname)
        conn.request("GET", "/dictionary/american/" + word)
        reason = conn.getresponse()
        data = reason.read()
        text = data.decode()
    else:
        f = open("file.htm")
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


# text = get_html_for_word("do")
# text = get_related_for_word("do")
text = get_syn_for_word("do")

root = etree.HTML(text)

# print(root.xpath('//meta[@name="viewport"]/@content'))
# print(root.xpath('//body/div[@id="wrapper"]/div[@class="content english"]/div[@class="dictionary"]'
#     '/div[@class="definition_wrapper english"]/div[@class="definition_main"]/div[@class="definition_content col main_bar"]'
#     ''))

print_children(root, padding=0)

# traverse_children(root, None)