from lxml import etree
from .etree_printer import *
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
            text = " ".join([x.text for x in elems if len(x.text) > 0])
            return text

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

        if len(results) == 0:
            results = sslist_etree.xpath('./*[re:match(@class, "sense_list_item level_\d")]',  # 11 KEYS or 13 KEYS
                                         namespaces={"re": "http://exslt.org/regular-expressions"})
            assert(len(results) == 1)
            assert "value" not in results[0].keys()

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
                results = results + text_elems

            else:
                results.append(text)

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

    @staticmethod
    def _parse_hi(node: etree._Element) -> str:
        text = ""

        if node.text is not None:
            text += node.text
        if node.tail is not None:
            text += node.tail
        return text

    @staticmethod
    def _parse_xr_ref(elem: etree._Element) -> str:
        assert elem.text is None
        assert elem.tail is None

        xr_ref_link = elem.xpath("./*[@class='xr_ref_link']")[0]
        assert xr_ref_link.text is not None
        assert xr_ref_link.tail is None

        text = xr_ref_link.text
        # print("xr ref text: ", text)
        href = xr_ref_link.get("href")
        word_def = re.match("[\w-]+#[\w-]+_(\d)", href)

        assert len(word_def.groups()) == 1
        word_def = word_def.groups()[0]

        text += " (def. {})".format(word_def)
        # print("xr ref return: ", text)
        return text

    @staticmethod
    def _parse_xr(elem: etree._Element) -> str:
        text = ""
        tail = ""

        if elem.text is not None:
            # print("xr text: ", elem.text)
            text += elem.text

        if len(elem.getchildren()):
            # print("xr has children...")
            pass

        for child in elem.getchildren():
            assert len(child.keys()) == 1
            key = child.keys()[0]

            # print("xr child: ({}, {})".format(key, child.get(key)))

            if key == "class" and child.get(key) == "lbl":
                if child.text is not None:
                    # print("xr lbl text: ", child.text)
                    text += child.text
                if child.tail is not None:
                    # print("xr lbl tail: ", child.tail)
                    text += child.tail

            elif key == "class" and child.get(key) == "xr_ref":
                xr_href_text = DictParser._parse_xr_ref(child)
                # print("xr_href_text: ", xr_href_text)
                text += xr_href_text

        if elem.tail is not None:
            # print("xr tail: ", elem.tail)
            text += elem.tail

        return text

    @staticmethod
    def _parse_lbl(elem: etree._Element, use_tail=True) -> (str, str):
        # print("label: ", elem.get(elem.keys()[0]))

        text = ""
        tail = ""

        if elem.text is not None:
            # print("label text: ", elem.text)
            text += elem.text

        hi_nodes = elem.xpath('./*[@class="hi"]')
        if len(hi_nodes):
            # print("have hi nodes in label!")
            pass

        for node in hi_nodes:
            hi_text = DictParser._parse_hi(node)
            text += hi_text
            # print("found hi text: ", hi_text)

        if elem.tail is not None:
            if use_tail:
                # print("label tail: ", elem.tail)
                text += elem.tail
            else:
                # print("tail 'ignored': ", elem.tail)
                tail = elem.tail

        return text, tail

    # GET-s
    def get_word_freq(self) -> str:
        elems = self.sidebar_elem.xpath('./*[@class="commonness"]/'                      # 7 KEYS
                                       '*[@title]')                                      # 8 KEYS

        if len(elems):
            return elems[0].get("title")

        return ""

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

    def get_all_derived_forms(self, def_group):
        # may be null.
        re_hom_subsecs = def_group.xpath('./*[@class="homograph-entry"]/'         # 8 KEYS
                                         '*[@class="re hom-subsec"]')           # 9 KEYS

        der_forms = {}
        for item in re_hom_subsecs:
            gram_values = item.xpath('./*[@class="gramGrp"]/'
                                    '*[@class="pos"]/text()')
            if len(gram_values) == 0:
                continue

            gram_value = gram_values[0]
            derived_form = item.xpath('./*[@class="drv"]/text()')[0]
            derived_form = derived_form.replace("ˈ", "")

            if gram_value in der_forms:
                der_forms[gram_value] += ", " + derived_form
            else:
                der_forms[gram_value] = derived_form

            derived_forms = item.xpath('./*[@class="hom"]/*[@class="var"]/*[@class="var"]/text()')

            if len(derived_forms):
                der_forms[gram_value] += " " + derived_forms[0].replace("ˈ", "")

        if der_forms == {}:
            return None

        return der_forms

    def get_all_nearby_words(self):
        results = []
        nby_elems = self.sidebar_elem.xpath('./*[@class="nearby_entries"]//'     # 7 KEYS
                               'li/'                                             # 10 KEYS
                                'a')                                             # 11 KEYS

        for nby_elem in nby_elems:
            results.append(nby_elem.text)

        return results

    def get_all_translations(self):
        results = self.mainbar_elem.xpath('./*[@id="translations_box"]/'          # 7 KEYS
                                         '*[@id="translations-content"]/'        # 8 KEYS
                                         '*[@class="translation_list clear"]')   # 9 KEYS

        list_results = []
        for item in results:
            text = ""
            subitems = item.xpath('./*[@class="translation"]/'
                                 '*[@class="hom lang_EN-US"]/'
                                 '*[@class="hi"]')

            for subitem in subitems:
                begin_item = subitem.getprevious()

                if "class" in begin_item.keys() and begin_item.get("class") == "neutral":
                    if begin_item.tail is not None:
                        text += begin_item.tail

                subtext = ""
                if len(subitem.getchildren()):
                    assert len(subitem.getchildren()) == 1
                    child = subitem.getchildren()[0]

                    if "class" in child.keys() and child.get("class") == "neutral":
                        if child.text is not None:
                            subtext += child.text
                        if child.tail is not None:
                            subtext += child.tail

                text += subtext

                if subitem.text is not None:
                    text += subitem.text

                if subitem.tail is not None:
                    if len(subtext):
                        text += " --- "
                    text += subitem.tail

            list_results.append(text)

        return list_results

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
            text = " ".join([x.text for x in elems])
            return text

        return ""

    @staticmethod
    def get_word_forms(ggroup):
        elems = ggroup.xpath('./*[@class="inflected_forms"]/'                 # 11 KEYS
                             '*[@class="infl"]')                              # 12 KEYS

        result = []
        for e in elems:
            # t = e.text.replace("ˈ", "'")
            t = e.text.replace("ˈ", "")
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
        assert isinstance(elem, etree._Element)

        text = elem.text if elem.text is not None else ""
        tail = elem.tail if elem.tail is not None else ""
        # print("DEFINITION text='{}'; tail='{}'".format(text, tail))

        text += tail

        # TODO: what is THIS??
        text_r = elem.xpath('./*[@class="hi"] | ./strong')

        for y in text_r:
            if y.text is not None:
                # print("text_r text: ", y.text)
                text += y.text
            if y.tail is not None:
                # print("text_r tail: ", y.tail)
                text += y.tail

        next_elem = elem.getnext()

        while next_elem is not None:
            assert len(next_elem.keys()) == 1

            key = next_elem.keys()[0]
            # print("next: ({}, {})".format(key, next_elem.get(key)))
            if key == "class" and re.match("lbl .+", next_elem.get(key)):
                addit_text = DictParser._parse_lbl(next_elem)
                # print("label addit text: ", addit_text)

                text += addit_text[0]

            elif key == "class" and next_elem.get(key) == "xr":
                xr_text = DictParser._parse_xr(next_elem)
                # print("called xr: text=", xr_text)

                text += xr_text

            next_elem = next_elem.getnext()

        text = text.strip()
        text = text.replace("\n", "")
        text = re.sub(' +', ' ', text)

        # if len(text) == 0:
        hrlinks = elem.xpath('.//*[@class="xr_ref_link"]')
        if len(hrlinks):
            assert len(hrlinks) == 1
            hrlink = hrlinks[0]

            text = hrlink.text

            link = hrlink.get("href")
            word_def = re.match("\w+#\w+_(\d)", link)
            assert len(word_def.groups()) == 1
            word_def = word_def.groups()[0]

            text += " (def. {})".format(word_def)
        # return text

        # print("------ DEFINITION")

        return text

    @staticmethod
    def get_definition_categ(sense_list_item):
        assert sense_list_item.getchildren()
        text = ""

        # print("CATEG")

        child = sense_list_item.getchildren()[0]
        label_tail = ""
        while child is not None:
            # print("child is not none")
            keys = child.keys()
            assert len(keys) == 1
            key = keys[0]

            if key != "class" or not re.match("lbl .+", child.get(key)):
                break

            # add the previous tail
            text += label_tail

            label_text, label_tail = DictParser._parse_lbl(child, use_tail=False)
            text += label_text

            child = child.getnext()

        # print("categ text: ", text)
        return text

    @staticmethod
    def get_def_example(sense_list_item):
        results = sense_list_item.xpath('./*[@class="orth"]//text()')   # 13 KEYS or 15 KEYS
        text_results = "".join(results)

        text = "".join(x for x in text_results if ord(x) < 128)
        text = re.sub(" +", ' ', text)
        text = text.strip()

        return text

