from lxml import etree
import re

from src.html_item import *


class LearnParser:
    def __init__(self, root, word_name):
        self.root = root
        self.word_name = word_name

        self.page = self.root.xpath('//div[@class="homograph-entry"]/'                                # 6
                                    'div[@class=" page"]')[0]

        cobuild_dict = self.root.xpath('//*[@class="Cob_Adv_Brit dictionary"]')  # KEY 9 (definitions)
        assert(len(cobuild_dict) == 1)
        self.cobuild_dict = cobuild_dict[0]

    def get_cobuild_dict(self):
        return self.cobuild_dict

    def get_all_def_groups(self):
        # returns all items of kind:
        #       KEYS: (div) class=" dictentry"; type="full"
        return self.cobuild_dict.getchildren()

    @staticmethod
    def get_def_group_text(def_group):
        h1_items = def_group.xpath('.//*[@class="h1_entry"]')
        assert(len(h1_items) == 1)

        # the normal one in the header: always there
        text = ParentHtmlItem(h1_items[0], strip=True).read()

        # for "do" (and on the second line, "or do a"), we must filter -- anything with a key that is not a " pron"
        # these are siblings of h1_entry, children of def_group (div[@class="entry_header"]) also.
        for item in h1_items[0].itersiblings():
            if len(item.keys()) == 0:
                continue
            if "class" in item.keys() and item.get("class") == " pron":
                continue
            text += HtmlItem(item, strip=True).read()

        return text

    @staticmethod
    def get_note(def_group: etree._Element):
        note_item = def_group.xpath('.//*[@class=" note"]')
        assert len(note_item) <= 1

        if len(note_item) == 0:
            return None

        return ParentHtmlItem(note_item[0]).read()

    @staticmethod
    def get_all_grammar_groups(def_group: etree._Element):
        groups = def_group.xpath('.//div[@class="content definitions cobuild br"]/*[@class=" hom"]')
        return groups

    @staticmethod
    def get_gram_value(gram_group: etree._Element):
        items = gram_group.xpath('./*[@class=" gramGrp"]')
        if len(items) == 0:
            return ""

        assert len(items) == 1

        text = ParentHtmlItem(items[0], strip=True).read()
        # NOTE: can be --- 'value': 'the internet domain name\n                    for'
        # so we must remove spaces and '\n' chars
        text = re.sub(r' +', ' ', text)
        text = text.replace('\n', '')
        return text

    @staticmethod
    def get_word_forms(def_group: etree._Element):
        text_items = def_group.xpath('.//*[@class="inflected_forms form"]/*[@class=" orth"]/text()')
        return text_items

    @staticmethod
    def get_all_sense_items(gram_group: etree._Element):
        items = gram_group.xpath('./*[@class=" sense"]')
        return items

    @staticmethod
    def get_sense_def(sense_item: etree._Element):
        items = sense_item.xpath('./*[@class=" def"]')
        assert len(items) <= 1

        if len(items) == 0:
            # we have a subgroup, most likely!
            return None

        def_item = items[0]

        text = ParentHtmlItem(def_item).read()
        return text

    @staticmethod
    def get_sense_def_label(sense_item: etree._Element):
        items = sense_item.xpath('./*[@class=" xr"]')
        assert len(items) <= 1

        if len(items) == 0:
            # we have a subgroup, most likely!
            return ""

        def_item = items[0]

        # might be HtmlItem simple, but we can't promise!
        text = ParentHtmlItem(def_item).read()
        # text = "(i) " + text
        return text

    @staticmethod
    def get_sense_example(sense_item: etree._Element):
        return sense_item.xpath('./*[@class=" exmplgrp"]/*[@class=" quote"]/text()')

    @staticmethod
    def get_sense_categ(sense_item: etree._Element):
        items = sense_item.xpath('./*[@class=" lbl" and @type]')

        if len(items) == 0:
            return ""

        text_list = [ParentHtmlItem(usage_item).read() for usage_item in items]
        # we may have ' informal ' or the like.
        text = "".join(text_list).strip()
        # the categories (in learner's) is normally "[category]"
        if text.startswith("[") and text.endswith("]"):
            text = text[1:-1]

        return text
