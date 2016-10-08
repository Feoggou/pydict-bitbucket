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
        syn_line = list()
        syn_text = categ = ""

        for item in sense_item.getchildren():
            categ, syn_text, result = SynParser._read_syn_or_opp(categ, item, syn_text, "syn")

            if result is not None and result != ():
                syn_line = [x for x in syn_line if x[0] != result[0]]
                syn_line.append(result)

            if categ is None and syn_text is None:
                # we reached the opposites => have already reached the end and have all.
                return SynParser.syn_opp_result(syn_line)

        if categ != "":
            last_item = (syn_text, categ)
            syn_line = [x for x in syn_line if x[0] != syn_text]
            syn_line.append(last_item)

        result = SynParser.syn_opp_result(syn_line)

        return result

    @staticmethod
    def syn_opp_result(line: list):
        result = []
        for syn_item in line:
            item = {syn_item[0]: syn_item[1]}
            result.append(item)
        return result

    @staticmethod
    def get_opp_line(sense_item: etree._Element):
        opp_line = list()
        opp_text = categ = ""

        scbold_items = sense_item.xpath('./span[@class="scbold"]')
        if len(scbold_items) == 0:
            return ""

        assert len(scbold_items) == 1

        # sense_item.
        for item in scbold_items[0].itersiblings():
            categ, opp_text, result = SynParser._read_syn_or_opp(categ, item, opp_text, "ant")

            if result is not None and result != ():
                opp_line = [x for x in opp_line if x[0] != result[0]]
                opp_line.append(result)

        if categ != "":
            last_item = (opp_text, categ)
            opp_line = [x for x in opp_line if x[0] != opp_text]
            opp_line.append(last_item)

        return SynParser.syn_opp_result(opp_line)

    @staticmethod
    def _read_syn_or_opp(categ: str, item: etree._Element, text: str, class_value: str):
        if "class" in item.keys() and "scbold" == item.get("class"):
            return None, None, None

        result = ()

        if "class" in item.keys() and re.match("lbl.*", item.get("class")):
            # HERE we check category
            categ = SynParser._update_categ(categ, item)

            if item.tail is not None:
                if item.tail.startswith("),") or item.tail.startswith(") •") or item.tail.startswith(")\n"):
                    result = (text, categ)
                    text = ""
                    categ = ""

        elif "class" in item.keys() and item.get("class") == class_value:
            # HERE we check the synonym
            text = ParentHtmlItem(item, use_tail=False, strip=True).read()
            result = (text, "")

            if item.tail is not None:
                if item.tail.startswith(",") or item.tail.startswith(" •"):
                    result = (text, categ)
                    text = ""
                    categ = ""

        return categ, text, result

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
            items = sense_item.xpath('./div[@class="cit"]/span[@class="orth"]/q/text()')
            assert len(items) <= 1

            if len(items) == 0:
                return ""

        return "; ".join(items)
