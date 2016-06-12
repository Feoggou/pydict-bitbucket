from lxml import etree
import re

from src.html_item import *


class SynParser:
    def __init__(self, root, word_name):
        self.root = root
        self.word_name = word_name

        self.homo_entry = self.root.xpath('//div[@class="homograph-entry"]')[0]

    def get_def_group_text(self):
        h1_entries = self.homo_entry.xpath('.//*[@class="orth h1_entry"]')
        assert(len(h1_entries) == 1)

        text = HtmlItem(h1_entries[0]).read()
        text = text.replace("\n", "").strip()

        return text

    def get_all_grammar_groups(self):
        groups = self.homo_entry.xpath('./div[@class="content-box content-box-thesaurus"]/*[@class="hom"]')
        return groups

    @staticmethod
    def get_gram_value(gram_group: etree._Element):
        text_items = gram_group.xpath('.//*[@class="pos"]/text()')
        text = "".join(text_items)
        return text

    @staticmethod
    def get_all_sense_items(gram_group: etree._Element):
        items = gram_group.xpath('./ol[re:match(@class, "sense_list level_\d+")]/'
                                 'li[re:match(@class, "sense_list_item level_\d+")]',
                                 namespaces={"re": "http://exslt.org/regular-expressions"})
        return items

    @staticmethod
    def get_syn_line(sense_item: etree._Element):
        syn_line = dict()
        syn_text = categ = ""

        for item in sense_item.getchildren():
            if "class" in item.keys() and re.match("lbl.*", item.get("class")):
                # HERE we check category
                categ = SynParser._update_categ(categ, item)

                if item.tail is not None:
                    if item.tail.startswith("),") or item.tail.startswith(") •"):
                        syn_line[syn_text] = categ
                        syn_text = ""
                        categ = ""

            elif "class" in item.keys() and item.get("class") == "syn":
                # HERE we check the synonym
                syn_text = ParentHtmlItem(item, use_tail=False, strip=True).read()
                syn_line[syn_text] = ""

                if item.tail is not None:
                    if item.tail.startswith(",") or item.tail.startswith(" •"):
                        syn_line[syn_text] = categ
                        syn_text = ""
                        categ = ""

        return syn_line

    @staticmethod
    def _update_categ(categ, item):
        categ_text = HtmlItem(item, use_tail=False).read()
        if len(categ) == 0:
            categ = categ_text
        else:
            # we've got a group of categ items, the left side may end in ' ', or the right side might begin with ' '
            if categ.endswith(' ') or categ_text.startswith(' '):
                categ += categ_text
            else:
                categ += ", " + categ_text
        return categ

    @staticmethod
    def get_syn_example(sense_item: etree._Element):
        items = sense_item.xpath('./*[@class="orth"]//quote/text()')
        assert len(items) <= 1

        if len(items) == 0:
            return ""

        return "; ".join(items)
