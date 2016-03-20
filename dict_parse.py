from lxml import etree
from etree_printer import *
import re


class DictSynParser:
    def __init__(self, root, word_name):
        self.root = root
        self.word_name = word_name
        assert isinstance(self.root, etree._Element)

        self.main_elem = self.root.xpath('//*[@class="definition_main"]')[0]    # 5 KEYS
        assert isinstance(self.main_elem, etree._Element)

        self.mainbar_elem = self.main_elem.xpath('//*[@class="definition_content col main_bar"]')[0]    # 6 KEYS

        assert isinstance(self.mainbar_elem, etree._Element)

    def get_def_main(self):
        return self.main_elem

    @staticmethod
    def get_word_form_for_def_group(def_group):
        elem = def_group.xpath('./*[@class="homograph-entry"]/'              # 8 KEYS
                               '*[@class="orth h1_entry"]')[0]               # 9 KEYS

        child_elems = elem.xpath('./*[@class="italics"]')
        if len(child_elems):
            text = elem.text + child_elems[0].text + child_elems[0].tail
            text = text.replace("\n", "")
            return text
        else:
            return elem.text

    def get_all_def_groups(self):
        id_name_re = '"{}_\d"'.format(self.word_name)
        result = self.mainbar_elem.xpath('./*[re:match(@id, ' + id_name_re + ')]',             # 7 KEYS NOTE: okay!
                                 namespaces={"re": "http://exslt.org/regular-expressions"})

        return result

    @staticmethod
    def _get_all_home_subsecs(def_group):
        elems = def_group.xpath('./*[@class="homograph-entry"]/'              # 8 KEYS
                           '*[@class="similar-words hom-subsec"]')              # 9 KEYS

        return elems

    @staticmethod
    def get_all_grammar_groups(def_group):
        homss = DictSynParser._get_all_home_subsecs(def_group)[0]

        elems = homss.xpath('./*[@class="hom"]')                                # 10 KEYS

        return elems

    @staticmethod
    def get_all_grammar_values(def_group):
        homss = DictSynParser._get_all_home_subsecs(def_group)[0]

        elems = homss.xpath('./*[@class="hom"]/'                                # 10 KEYS
                            '*[@class="gramGrp h2_entry"]/'                     # 11 KEYS
                            '*[@class="pos"]')                                  # 12 KEYS

        result = [elem.text for elem in elems]
        return result

    @staticmethod
    def get_gram_value(gram_group):
        elems = gram_group.xpath('./*[@class="gramGrp h2_entry"]/'                   # 11 KEYS
                                '*[@class="pos"]')                               # 12 KEYS

        if len(elems):
            return elems[0].text

        return ""

    @staticmethod
    def get_senselist(grammar_group_elem):
        results = grammar_group_elem.xpath('./*[re:match(@class, "sense_list level_\d")]',      # 11 KEYS or 13 KEYS
                                           namespaces={"re": "http://exslt.org/regular-expressions"})
        if len(results):
            elem = results[0]
        else:
            elem = None

        return elem

    @staticmethod
    def get_senselist_item(sslist_etree, value):
        results = sslist_etree.xpath('./*[re:match(@class, "sense_list_item level_\d") '  # 11 KEYS or 13 KEYS
                            'and @value="' + value + '"]',
                             namespaces={"re": "http://exslt.org/regular-expressions"})
        elem = results[0]

        return elem

    @staticmethod
    def get_all_senselist_items(sslist_etree):
        results = sslist_etree.xpath('./*[re:match(@class, "sense_list_item level_\d")]', # 11 KEYS or 13 KEYS
                             namespaces={"re": "http://exslt.org/regular-expressions"})

        return results

    @staticmethod
    def get_synonyms(sense_list_item):
        results = []

        syn_classes = sense_list_item.xpath('./*[@class="syn"]')
        for syn_cls in syn_classes:
            links = syn_cls.xpath('./*[@class="xr_ref"]')
            if len(links):
                text_elems = syn_cls.xpath('./*[@class="xr_ref"]/'
                                           'a/text()')
                results = results + text_elems

            else:
                results.append(syn_cls.text)

        return results

    @staticmethod
    def get_synonyms_category(sense_list_item):
        results = sense_list_item.xpath('./*[re:match(@class, "lbl .+")]',          # 13 KEYS or 15 KEYS
                             namespaces={"re": "http://exslt.org/regular-expressions"})
        if len(results) == 0:
            return ""

        text_items = []
        for x in results:
            text_r = x.xpath('./*[@class="hi"]')
            text = x.text
            for y in text_r:
                if y.text is not None:
                    text += y.text
                if y.tail is not None:
                    text += y.tail

            if len(text):
                text_items.append(text)

        text = " ".join([x for x in text_items])
        text = text.replace("  ", " ")

        return text


class DictRelatedParser:
    def __init__(self, root):
        self.root = root
        assert isinstance(self.root, etree._Element)

        self.main_elem = self.root.xpath('//*[@class="related_words_main main_bar col"]/'  # 4 KEYS
                                         '*[@class="columns"]')[0]                         # 5 KEYS

        assert self.main_elem is not None

    def get_def_main(self):
        return self.main_elem

    def get_all_related_words(self):
        items = self.main_elem.xpath('./*[@class="column"]//'    # 6 KEYS
                                     '*[@class="row"]/'          # 8 KEYS
                                     'a/text()')                # 9 KEYS

        # print("items=", items)
        return items


class DictParser:
    def __init__(self, root, word_name):
        self.root = root
        self.word_name = word_name
        assert isinstance(self.root, etree._Element)

        self.main_elem = self.root.xpath('//*[@class="definition_main"]')[0]    # 5 KEYS
        assert isinstance(self.main_elem, etree._Element)

        self.mainbar_elem = self.main_elem.xpath('//*[@class="definition_content col main_bar"]')[0]    # 6 KEYS
        self.sidebar_elem = self.main_elem.xpath('//*[@class="definition_sidebar col side_bar"]')[0]    # 6 KEYS

        assert isinstance(self.mainbar_elem, etree._Element)
        assert isinstance(self.sidebar_elem, etree._Element)

    # GET-s
    def get_word_freq(self) -> str:
        elem = self.sidebar_elem.xpath('./*[@class="commonness"]/'                      # 7 KEYS
                                       '*[@title]')[0]                                  # 8 KEYS

        return elem.get("title")

    def get_all_examples(self):
        results = []
        elems = self.mainbar_elem.xpath('./*[@id="examples_box"]/'              # 7 KEYS
                                        '*[@id="examples_box"]/*/'              # 8, 9 KEYS
                                        'blockquote')                           # 10

        for cur_elem in elems:
            text = cur_elem.text

            if text[0] == '"' and not text.endswith('"'):
                text = text[1:]

            results.append(text)

        return results

    def get_def_main(self):
        return self.main_elem

    def get_all_related_words(self, def_group):
        results = def_group.xpath('./*[@class="homograph-entry"]/'         # 8 KEYS
                                    '*[@class="re hom-subsec"]//'            # 9 KEYS
                                    '*[@class="xr_ref"]/a/text()')

        return results

    def get_all_nearby_words(self):
        results = []
        nby_elems = self.sidebar_elem.xpath('./*[@class="nearby_entries"]//'     # 7 KEYS
                               'li/'                                             # 10 KEYS
                                'a')                                             # 11 KEYS

        for nby_elem in nby_elems:
            results.append(nby_elem.text)

        return results

    def get_all_def_groups(self):
        id_name_re = '"{}_\d"'.format(self.word_name)
        result = self.mainbar_elem.xpath('./*[re:match(@id, ' + id_name_re + ')]',             # 7 KEYS NOTE: okay!
                                 namespaces={"re": "http://exslt.org/regular-expressions"})

        return result

    @staticmethod
    def get_word_form_for_def_group(def_group):
        elem = def_group.xpath('./*[@class="homograph-entry"]/'              # 8 KEYS
                               '*[@class="orth h1_entry"]')[0]               # 9 KEYS

        child_elems = elem.xpath('./*[@class="italics"]')
        if len(child_elems):
            text = elem.text + child_elems[0].text + child_elems[0].tail
            text = text.replace("\n", "")
            return text
        else:
            return elem.text

    @staticmethod
    def get_all_home_subsecs(def_group):
        elems = def_group.xpath('./*[@class="homograph-entry"]/'              # 8 KEYS
                           '*[@class="definitions hom-subsec"]')              # 9 KEYS

        return elems

    @staticmethod
    def get_all_grammar_groups(def_group):
        homss = DictParser.get_all_home_subsecs(def_group)[0]

        elems = homss.xpath('./*[@class="hom"]')                                # 10 KEYS

        return elems

    @staticmethod
    def get_all_grammar_values(def_group):
        homss = DictParser.get_all_home_subsecs(def_group)[0]

        elems = homss.xpath('./*[@class="hom"]/'                                # 10 KEYS
                            '*[@class="gramGrp h3_entry"]/'                     # 11 KEYS
                            '*[@class="pos"]')                                  # 12 KEYS

        result = [elem.text for elem in elems]
        return result

    @staticmethod
    def get_semantics(def_group):
        homss = DictParser.get_all_home_subsecs(def_group)[0]

        sems_items = homss.xpath('./*[@class="semantic"]')
        if len(sems_items) == 0:
            return None

        sems = sems_items[0]

        text = ""

        for item in sems.getchildren():
            if "class" in item.keys() and item.get("class") == "xr":
                subelement = item.xpath('./*[@class="xr_ref"]/a/text()')[0]
                text += subelement + item.tail
            elif "class" in item.keys() and item.get("class") == "hi":
                if item.text is not None:
                    text += item.text
                if item.tail is not None:
                    text += item.tail

        text = re.sub(' +', ' ', text)
        text = text.replace("\n", "")
        return text

    @staticmethod
    def get_gram_value(gram_group):
        elems = gram_group.xpath('./*[@class="gramGrp h3_entry"]/'                   # 11 KEYS
                                '*[@class="pos"]')                               # 12 KEYS

        if len(elems):
            return elems[0].text

        return ""

    @staticmethod
    def get_word_forms(ggroup):
        elems = ggroup.xpath('./*[@class="inflected_forms"]/'                 # 11 KEYS
                             '*[@class="infl"]')                              # 12 KEYS

        result = []
        for e in elems:
            t = e.text.replace("ˈ", "'")
            text = "".join(x for x in t if re.match("[^\s,]", x))   # ("[A-Za-z']", x))
            if len(text):
                result.append(text)

        return result

    @staticmethod
    def get_senselist(grammar_group_elem):
        results = grammar_group_elem.xpath('./*[re:match(@class, "sense_list level_\d")]',      # 11 KEYS or 13 KEYS
                                           namespaces={"re": "http://exslt.org/regular-expressions"})
        if len(results):
            elem = results[0]
        else:
            elem = None

        return elem

    @staticmethod
    def get_senselist_item(sslist_etree, value):
        results = sslist_etree.xpath('./*[re:match(@class, "sense_list_item level_\d") '  # 11 KEYS or 13 KEYS
                            'and @value="' + value + '"]',
                             namespaces={"re": "http://exslt.org/regular-expressions"})
        elem = results[0]

        return elem

    @staticmethod
    def get_all_senselist_items(sslist_etree):
        results = sslist_etree.xpath('./*[re:match(@class, "sense_list_item level_\d")]', # 11 KEYS or 13 KEYS
                             namespaces={"re": "http://exslt.org/regular-expressions"})

        return results

    @staticmethod
    def get_definition(sense_list_item):
        results = sense_list_item.xpath('./*[@class="def"]')   # 13 KEYS or 15 KEYS
        elem = results[0]

        text_r = elem.xpath('./*[@class="hi"]')
        text = elem.text
        for y in text_r:
            if y.text is not None:
                text += y.text
            if y.tail is not None:
                text += y.tail

        text = text.strip()
        text = text.replace("\n", "")
        text = re.sub(' +', ' ', text)

        if len(text) == 0:
            hrlink = elem.xpath('.//*[@class="xr_ref_link"]')[0]
            return hrlink.text

        return text

    @staticmethod
    def get_definition_categ(sense_list_item):
        results = sense_list_item.xpath('./*[re:match(@class, "lbl .+")]',          # 13 KEYS or 15 KEYS
                             namespaces={"re": "http://exslt.org/regular-expressions"})
        if len(results) == 0:
            return ""

        text_items = []
        for x in results:
            text_r = x.xpath('./*[@class="hi"]')
            text = x.text
            for y in text_r:
                if y.text is not None:
                    text += y.text
                if y.tail is not None:
                    text += y.tail

            if len(text):
                text_items.append(text)

        text = ", ".join([x for x in text_items])
        text = text.replace("  ", " ")

        return text

    @staticmethod
    def get_def_example(sense_list_item):
        results = sense_list_item.xpath('./*[@class="orth"]//text()')   # 13 KEYS or 15 KEYS
        text_results = "".join(results)

        text = "".join(x for x in text_results if ord(x) < 128)
        text = re.sub(" +", ' ', text)
        text = text.strip()

        return text

