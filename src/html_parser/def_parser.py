from lxml import etree
import re

from . import html_parser


class HtmlItem:
    def __init__(self, etree_item: etree._Element):
        self.item = etree_item
        # print("text: '{}'".format(etree_item.text))
        # print("tail: '{}'".format(etree_item.tail))

        self.text = etree_item.text if etree_item.text is not None else ""
        self.tail = etree_item.tail if etree_item.tail is not None else ""

    def read(self):
        text = self.text

        text += self.tail

        return text


class HtmlItemCreator:
    ALL_TAGS = None
    ALL_KEYS = None
    ALL_CLASSES = None

    def __init__(self):
        HtmlItemCreator.ALL_TAGS = {
            "strong": HtmlItemCreator.create_default_item,
            "em": HtmlItemCreator.create_default_item,
            "span": HtmlItemCreator.create_keys_item,
            "a": HtmlItemCreator.create_a_href_item,
            "sup": HtmlItemCreator.create_sup_item,
            "br": HtmlItemCreator.create_br_item,
        }

        HtmlItemCreator.ALL_KEYS = {"class": HtmlItemCreator.create_class_item}

        HtmlItemCreator.ALL_CLASSES = {
            "xr": ParentHtmlItem,  # XrItem,
            "xr_ref": ParentHtmlItem,  # XrRefItem,
            "xr_ref_link": XrRefLinkItem,
            "lbl register": ParentHtmlItem,  # LblRegisterItem,
            "lbl": HtmlItem,
            "orth": HtmlItemCreator.create_nothing,
        }

    @staticmethod
    def create_default_item(elem):
        return HtmlItem(elem)

    @staticmethod
    def create_sup_item(elem):
        return SupItem(elem)

    @staticmethod
    def create_br_item(elem):
        return BrItem(elem)

    @staticmethod
    def create_a_href_item(elem):
        assert len(elem.keys()) == 2
        # key = elem.keys()[0]

        return HtmlItemCreator.ALL_KEYS["class"](elem)

    @staticmethod
    def create_keys_item(elem):
        assert len(elem.keys()) == 1
        key = elem.keys()[0]

        return HtmlItemCreator.ALL_KEYS[key](elem)

    @staticmethod
    def create_nothing(elem):
        return None

    @staticmethod
    def create_class_item(elem):
        class_name = elem.get("class")
        print("class: ", class_name)

        # if class_name in HtmlItemCreator.ALL_CLASSES:
        return HtmlItemCreator.ALL_CLASSES[class_name](elem)

        # return None

    @staticmethod
    def create_tag_item(elem):
        print("create tag item: tag='{}'; keys='{}'; values='{}'; text='{}'; tail='{}'"
              .format(elem.tag, elem.keys(), elem.values(), elem.text, elem.tail))
        return HtmlItemCreator.ALL_TAGS[elem.tag](elem)


class ParentHtmlItem(HtmlItem):
    def __init__(self, etree_item: etree._Element):
        HtmlItem.__init__(self, etree_item)
        self.creator = HtmlItemCreator()

    def read(self):
        text = self.text
        text += self.read_children()
        text += self.tail

        return text

    def read_children(self):
        text = ""
        for e in self.item.getchildren():
            item = self.creator.create_tag_item(e)
            # item = ALL_TAGS[e.tag](e)
            text += item.read()
        return text


class XrRefLinkItem(ParentHtmlItem):
    def __init__(self, etree_item: etree._Element):
        ParentHtmlItem.__init__(self, etree_item)
        assert self.item.text is not None
        assert self.item.tail is None

        print("xr_ref_link: text='{}'; tail='{}'".format(self.text, self.tail))

    def read(self):
        text = self.text

        href = self.item.get("href")
        word_def = re.match("[\w-]+#[\w-]+_(\d)", href)

        assert len(word_def.groups()) == 1
        word_def = word_def.groups()[0]
        text += "[{}]".format(word_def)

        text += self.read_children()

        text += self.tail

        return text


class SupItem(HtmlItem):
    def __init__(self, etree_item: etree._Element):
        HtmlItem.__init__(self, etree_item)

    def read(self):
        return "({}{})".format(self.text, self.tail)


class BrItem(HtmlItem):
    def __init__(self, etree_item: etree._Element):
        HtmlItem.__init__(self, etree_item)

    def read(self):
        return "; "


class DefItem(ParentHtmlItem):
    def __init__(self, etree_item: etree._Element):
        ParentHtmlItem.__init__(self, etree_item)
        print("def: text='{}'; tail='{}'".format(self.text, self.tail))

    def read(self):
        text = ParentHtmlItem.read(self)
        text += self.read_siblings()

        return text

    def read_siblings(self):
        text = ""
        for next_elem in self.item.itersiblings():
            item = self.creator.create_tag_item(next_elem)  # create_class_item(next_elem)
            if item is not None:
                text += item.read()

        return text


class DefParser(html_parser.HtmlParser):
    def __init__(self, root, word_name, fake: bool = False):
        if fake:
            self.word_name = word_name
            return

        html_parser.HtmlParser.__init__(self, root, word_name)
        self.sidebar_elem = self.main_elem.xpath('//*[@class="definition_sidebar col side_bar"]')[0]    # 6 KEYS

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

        xr_ref_link = elem.xpath("./*[@class='xr_ref_link']")[0]
        assert xr_ref_link.text is not None
        assert xr_ref_link.tail is None

        text = xr_ref_link.text
        # print("xr ref text: ", text)
        href = xr_ref_link.get("href")
        word_def = re.match("[\w-]+#[\w-]+_(\d)", href)

        assert len(word_def.groups()) == 1
        word_def = word_def.groups()[0]

        text += "[{}]".format(word_def)

        if len(xr_ref_link.getchildren()):
            for child in xr_ref_link.getchildren():
                if len(child.keys()):
                    # print("child keys: ", child.keys())
                    assert child.get("class") == "hi"
                    child_text = DefParser._parse_hi(child)
                    text += child_text

        if elem.tail is not None:
            text += elem.tail
        # print("xr ref return: ", text)
        return text

    @staticmethod
    def _parse_xr(elem: etree._Element) -> str:
        text = ""
        # tail = ""

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
                xr_href_text = DefParser._parse_xr_ref(child)
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
            hi_text = DefParser._parse_hi(node)
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

        if len(elems) == 0:
            return ""

        full_text = elems[0].get("title")
        return full_text.partition(".")[0]

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
            derived_forms = item.xpath('./*[@class="drv"]/text()')
            if len(derived_forms) > 0:
                derived_form = derived_forms[0]
            else:
                derived_forms = item.xpath('.//*[@class="infl"]/text()')
                derived_form = "".join(derived_forms)

            derived_form = derived_form.replace("ˈ", "").replace("ˌ", "")
            derived_form = derived_form.replace("ˌ", "")
            derived_form = derived_form.replace(" ", " ")
            derived_form = re.sub(' +', ' ', derived_form)

            if gram_value in der_forms:
                der_forms[gram_value] += ", " + derived_form
            else:
                der_forms[gram_value] = derived_form

            derived_forms = item.xpath('./*[@class="hom"]/*[@class="var"]/*[@class="var"]/text()')

            if len(derived_forms):
                der_forms[gram_value] += " " + derived_forms[0].replace("ˈ", "").replace("ˌ", "")

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

    def _get_homsubsec_name(self):
        return "definitions"

    def _get_gramgroup_name(self):
        return "gramGrp h3_entry"

    def get_semantics(self, def_group):
        homss = self.get_all_home_subsecs(def_group)[0]

        sems_items = homss.xpath('./*[@class="semantic"]')
        if len(sems_items) == 0:
            return None

        if len(sems_items) > 1:
            print("HAVE MANY SEMANTICS: EXPECTED 1!")

        sems = sems_items[0]

        text = sems.text if sems.text is not None and len(sems.text.strip()) > 0 else ""

        for item in sems.getchildren():
            if "class" in item.keys() and item.get("class") == "xr":
                subelement = item.xpath('./*[@class="xr_ref"]/a/text()')[0]
                text += subelement
                if item.tail is not None:
                    text += item.tail
            elif "class" in item.keys() and item.get("class") == "hi":
                if item.text is not None:
                    text += item.text
                if item.tail is not None:
                    text += item.tail

        text = re.sub(' +', ' ', text)
        text = text.replace("\n", "")
        return text

    @staticmethod
    def get_word_forms(ggroup):
        elems = ggroup.xpath('./*[@class="inflected_forms"]/'                 # 11 KEYS
                             '*[@class="infl"]')                              # 12 KEYS

        result = []
        for e in elems:
            if e.text is None:
                continue
            t = e.text.replace("ˈ", "").replace("ˌ", "")
            text = "".join(x for x in t if re.match("[^\s,]", x))   # ("[A-Za-z']", x))
            if len(text):
                result.append(text)

        return result

    @staticmethod
    def get_alternative_def(ggroup):
        etree_item = ggroup.xpath('./span')[0]

        item = DefItem(etree_item)
        text = item.read()
        print("alternative text: ", text)
        return text

    @staticmethod
    def get_definition(sense_list_item):
        text = ""
        results = sense_list_item.xpath('./*[@class="def"]')  # 13 KEYS or 15 KEYS
        if len(results) != 1:
            # raise RuntimeError("Expected 1 definition as 'class'='def', we got: ", len(results))
            results = sense_list_item.getchildren()

        elem = results[0]
        assert elem is not None
        assert isinstance(elem, etree._Element)

        item = DefItem(elem)
        text = item.read()

        text = re.sub(' +', " ", text)
        text = text.replace("\n", "")
        text = text.strip()

        return text

    @staticmethod
    def get_definition2(sense_list_item):
        results = sense_list_item.xpath('./*[@class="def"]')   # 13 KEYS or 15 KEYS
        if len(results) > 1:
            print(results)

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
            if len(next_elem.keys()) == 0:
                assert next_elem.tag == "br"
                text += " "
                next_elem = next_elem.getnext()
                continue

            assert len(next_elem.keys()) == 1

            key = next_elem.keys()[0]
            # print("next: ({}, {})".format(key, next_elem.get(key)))
            if key == "class" and re.match("lbl .+", next_elem.get(key)):
                addit_text = DefParser._parse_lbl(next_elem)
                # print("label addit text: ", addit_text)

                text += addit_text[0]

            elif key == "class" and next_elem.get(key) == "xr":
                xr_text = DefParser._parse_xr(next_elem)
                # print("called xr: text=", xr_text)

                text += xr_text

            next_elem = next_elem.getnext()

        text = text.strip()
        text = text.replace("\n", "")
        text = re.sub(' +', ' ', text)

        # if len(text) == 0:
        hrlinks = elem.xpath('.//*[@class="xr_ref_link"]')
        for hrlink in hrlinks:
            # if len(hrlinks):
            # assert len(hrlinks) == 1
            # hrlink = hrlinks[0]

            if len(text):
                text += " "
            text += hrlink.text

            link = hrlink.get("href")
            word_def = re.match("[A-Za-z0-9\- \.\']+#[A-Za-z0-9\- \.\']+_(\d)", link)
            assert len(word_def.groups()) == 1
            word_def = word_def.groups()[0]

            text += "[{}]".format(word_def)
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

            label_text, label_tail = DefParser._parse_lbl(child, use_tail=False)
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

