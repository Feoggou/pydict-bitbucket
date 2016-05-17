from lxml import etree
import re

from . import html_parser


class SynParser(html_parser.HtmlParser):
    def __init__(self, root, word_name):
        html_parser.HtmlParser.__init__(self, root, word_name)

    @staticmethod
    def get_word_form_for_def_group(def_group):
        # TODO: This is defined in HtmlParser, but we also take into account "else:" here
        elem = def_group.xpath('./*[@class="homograph-entry"]/'              # 8 KEYS
                               '*[@class="orth h1_entry"]')[0]               # 9 KEYS

        child_elems = elem.xpath('./*[@class="italics"]')
        if len(child_elems):
            text = elem.text + child_elems[0].text + child_elems[0].tail
            text = text.replace("\n", "")
            return text
        else:
            text = elem.text
            if len(elem.getchildren()) > 0:
                assert len(elem.getchildren()) == 1

                child = elem.getchildren()[0]
                if child.keys() == ["class"] and child.get("class") == "lbl register":
                    child_text = child.text
                    child_text += child.tail
                    child_text = child_text.replace("\n", "")

                    text += child_text

            return text

    def _get_homsubsec_name(self):
        return "similar-words"

    def _get_gramgroup_name(self):
        return "gramGrp h2_entry"

    @staticmethod
    def get_syn_category(item: etree._Element):
        categs = []
        last_is_tail = False

        while item is not None and "class" in item.keys() and re.match("lbl .+", item.get("class")):
            last_is_tail = False

            text_r = item.xpath('./*[@class="hi"]')
            # TODO: is it possible to have @class="hi"?
            text = item.text
            for y in text_r:
                if y.text is not None:
                    text += y.text
                if y.tail is not None:
                    text += y.tail

            text = text.replace("  ", " ")
            categs.append(text)
            if item.tail is not None:
                categs.append(item.tail)
                last_is_tail = True

            item = item.getnext()

        if last_is_tail:
            categs.pop()

        return "".join(categs)

    @staticmethod
    def get_synonyms(sense_list_item):
        results = []

        syn_classes = sense_list_item.xpath('./*[@class="syn"] | ./*[@class="phrase"]/*[@class="xr"]')
        for syn_cls in syn_classes:
            text = syn_cls.text if syn_cls.text is not None else ""
            text = text.strip()
            links = syn_cls.xpath('./*[@class="xr_ref"]')
            if len(links):
                text_elems = syn_cls.xpath('./*[@class="xr_ref"]/'
                                           'a/text()')
                if len(text):
                    text_elems[0] = text + " " + text_elems[0]
                assert len(text_elems) == 1
                text = text_elems[0]

            categ = SynParser.get_syn_category(syn_cls.getnext())

            syn_obj = {"syn": text}
            if len(categ):
                syn_obj["category"] = categ

            results.append(syn_obj)

        return results

    @staticmethod
    def get_synonyms_category(sense_list_item: etree._Element):
        results = []
        ends_in_tail = False
        for eitem in sense_list_item.getchildren():
            if "class" in eitem.keys() and re.match("lbl .+", eitem.get("class")):
                text = eitem.text
                results.append(text)
                ends_in_tail = False
                if eitem.tail is not None:
                    results.append(eitem.tail)
                    ends_in_tail = True
            else:
                break

        if len(results) == 0:
            return ""

        if ends_in_tail:
            results.pop()

        text = "".join(results)

        return text

