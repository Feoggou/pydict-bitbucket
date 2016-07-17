from collections import OrderedDict

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
        syn_line = OrderedDict()
        syn_text = categ = ""

        for item in sense_item.getchildren():
            categ, syn_text = SynParser._read_syn_or_opp(categ, item, syn_line, syn_text, "syn")
            if categ is None and syn_text is None:
                # we reached the opposites => have already reached the end and have all.
                return SynParser.syn_opp_result(syn_line)

        if categ != "":
            syn_line[syn_text] = categ

        result = SynParser.syn_opp_result(syn_line)

        print("syn line: ", syn_line)

        return result

    @staticmethod
    def syn_opp_result(line):
        result = []
        for word in line.keys():
            item = {word: line[word]}
            result.append(item)
        return result

    @staticmethod
    def get_opp_line(sense_item: etree._Element):
        opp_line = OrderedDict()
        opp_text = categ = ""

        scbold_items = sense_item.xpath('./span[@class="scbold"]')
        if len(scbold_items) == 0:
            return ""

        assert len(scbold_items) == 1

        # sense_item.
        for item in scbold_items[0].itersiblings():
            categ, opp_text = SynParser._read_syn_or_opp(categ, item, opp_line, opp_text, "ant")

        if categ != "":
            opp_line[opp_text] = categ

        return SynParser.syn_opp_result(opp_line)

    @staticmethod
    def _read_syn_or_opp(categ: str, item: etree._Element, line: OrderedDict, text: str, class_value: str):
        if "class" in item.keys() and "scbold" == item.get("class"):
            return None, None

        if "class" in item.keys() and re.match("lbl.*", item.get("class")):
            # HERE we check category
            categ = SynParser._update_categ(categ, item)

            if item.tail is not None:
                if item.tail.startswith("),") or item.tail.startswith(") •"):
                    line[text] = categ
                    text = ""
                    categ = ""

        elif "class" in item.keys() and item.get("class") == class_value:
            # HERE we check the synonym
            text = ParentHtmlItem(item, use_tail=False, strip=True).read()
            line[text] = ""

            if item.tail is not None:
                if item.tail.startswith(",") or item.tail.startswith(" •"):
                    line[text] = categ
                    text = ""
                    categ = ""

        return categ, text

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
