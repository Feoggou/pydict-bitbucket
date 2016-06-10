from lxml import etree
import re

# from . import html_parser2

IS_VERBOSE = False


def print_vb(*args):
    if IS_VERBOSE:
        print(args)


class HtmlItem:
    def __init__(self, etree_item: etree._Element):
        self.item = etree_item
        print_vb("text: '{}'".format(etree_item.text))
        print_vb("tail: '{}'".format(etree_item.tail))

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
            # "strong": HtmlItemCreator.create_default_item,
            # "em": HtmlItemCreator.create_default_item,
            "span": HtmlItemCreator.create_keys_item,
            "a": HtmlItemCreator.create_a_href_item,
            # "sup": HtmlItemCreator.create_sup_item,
            # "br": HtmlItemCreator.create_br_item,
        }

        HtmlItemCreator.ALL_KEYS = {
            "class": HtmlItemCreator.create_class_item,
            "href": HtmlItemCreator.create_a_href_item2,
        }

        HtmlItemCreator.ALL_CLASSES = {
            # "xr": ParentHtmlItem,  # XrItem,
            # "xr_ref": ParentHtmlItem,  # XrRefItem,
            # "xr_ref_link": XrRefLinkItem,
            # "lbl register": ParentHtmlItem,  # LblRegisterItem,
            " lbl": ParentHtmlItem,
            # "orth": HtmlItemCreator.create_nothing,
            "ref": ParentHtmlItem,  # don't know if it appears as parent, but it's better to make sure!
            " colloc": ParentHtmlItem,
            " hi": ParentHtmlItem,  # don't know if it appears as parent, but it's better to make sure!
            " subc": ParentHtmlItem,
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
        return HtmlItem(elem)

    @staticmethod
    def create_a_href_item2(elem):
        # assert len(elem.keys()) == 2
        # key = elem.keys()[0]

        return HtmlItemCreator.ALL_KEYS["class"](elem)

    @staticmethod
    def create_keys_item(elem):
        if len(elem.keys()) == 0:
            return ParentHtmlItem(elem)  # might be parent, might be ordinary (so far, ordinary)

        if len(elem.keys()) == 1:
            key = elem.keys()[0]
        else:
            if "class" in elem.keys():
                key = "class"
                pass
            else:
                raise NotImplementedError(
                    "Attempted to use create_keys_item with an item, multiple keys ({}), but we don't know which to pick!"
                        .format(elem.keys()))

        return HtmlItemCreator.ALL_KEYS[key](elem)

    @staticmethod
    def create_nothing(elem):
        return None

    @staticmethod
    def create_class_item(elem):
        class_name = elem.get("class")
        print_vb("class: ", class_name)

        # if class_name in HtmlItemCreator.ALL_CLASSES:
        return HtmlItemCreator.ALL_CLASSES[class_name](elem)

        # return None

    @staticmethod
    def create_tag_item(elem):
        print_vb("create tag item: tag='{}'; keys='{}'; values='{}'; text='{}'; tail='{}'"
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

        text = re.sub(r' +', ' ', text)

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

        print_vb("xr_ref_link: text='{}'; tail='{}'".format(self.text, self.tail))

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


"""class DefItem(ParentHtmlItem):
    def __init__(self, etree_item: etree._Element):
        ParentHtmlItem.__init__(self, etree_item)
        print_vb("def: text='{}'; tail='{}'".format(self.text, self.tail))

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

        return text"""


class DefParser:
    def __init__(self, root, word_name):
        self.root = root
        self.word_name = word_name

        self.page = self.root.xpath('//div[@class="homograph-entry"]/'                                # 6
                                    'div[@class=" page"]')[0]

        collins = self.root.xpath('//*[@class="Collins_Eng_Dict dictionary"]')  # KEY 9 (definitions)
        assert(len(collins) == 1)
        self.collins_dict = collins[0]

    def get_collins_dict(self):
        return self.collins_dict

    def get_all_def_groups(self):
        # returns all items of kind:
        #       KEYS: (div) class=" dictentry"; type="full"
        return self.collins_dict.getchildren()

    @staticmethod
    def get_def_group_text(def_group):
        h1_items = def_group.xpath('.//*[@class="h1_entry"]')
        assert(len(h1_items) == 1)

        # the normal one in the header: always there
        text_list = h1_items[0].xpath('./*[@class=" orth"]/text()')
        text = "".join(text_list)

        # for "do" (and on the second line, "or do a"), we must filter -- anything with a key that is not a " pron"
        # these are siblings of h1_entry, children of def_group (div[@class="entry_header"]) also.
        for item in h1_items[0].itersiblings():
            if len(item.keys()) == 0:
                continue
            if "class" in item.keys() and item.get("class") == " pron":
                continue
            text += HtmlItem(item).read()

        return text

    @staticmethod
    def get_word_freq(def_group):
        freq_phrases = def_group.xpath('.//*[@class="word-frequency-img"]')
        if len(freq_phrases) == 0:
            return ""

        freq_phrase = freq_phrases[0].get("title")
        # here, freq_phrase has value for key=title:
        #       title="Extremely Common. do is one of the 1000 most commonly used words in the Collins dictionary"
        freq_phrase = freq_phrase.split(".")[0]
        return freq_phrase

    def get_all_examples(self):

        examples_quotes = self.page.xpath('.//div[@class="content examples"]/'
                                          'span[@class=" cit" and @type="example"]/'
                                          'span[@class=" quote"]')
        if len(examples_quotes) == 0:
            return []

        results = []
        for ex_quote in examples_quotes:
            item = ParentHtmlItem(ex_quote)
            text = item.read()

            # each example is found with appended whitespace (' ')
            # so we need to strip unneeded text.
            text = text.strip()

            results.append(text)

        return results

    @staticmethod
    def get_all_grammar_groups(def_group: etree._Element):
        groups = def_group.xpath('.//div[@class="content definitions ced"]/*[@class=" hom"]')
        return groups

    @staticmethod
    def get_gram_value(gram_group: etree._Element):
        text_items = gram_group.xpath('./*[@class=" gramGrp"]/*[@class=" pos"]/text()')
        text = "".join(text_items)
        # NOTE: can be --- 'value': 'the internet domain name\n                    for'
        # so we must remove spaces and '\n' chars
        text = re.sub(r' +', ' ', text)
        text = text.replace('\n', '')
        return text

    @staticmethod
    def get_word_forms(gram_group: etree._Element):
        text_items = gram_group.xpath('./*[@class="inflected_forms form"]/*[@class=" orth"]/text()')
        return text_items

    @staticmethod
    def get_word_forms_info(gram_group: etree._Element):
        text_items = gram_group.xpath('./*[@class="inflected_forms form"]/*[@type="gram"]/text()')
        return "".join(text_items)

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
        """if "type" in def_item.keys() and def_item.get("type") == "register":
            return None"""

        # might be HtmlItem simple, but we can't promise!
        text = ParentHtmlItem(def_item).read()
        # text = "(i) " + text
        return text

    @staticmethod
    def get_sense_example(sense_item: etree._Element):
        items = sense_item.xpath('./*[@class=" cit" and @type="example"]')
        assert len(items) <= 1

        if len(items) == 0:
            return ""

        cit_item = items[0]

        examples = cit_item.xpath('./*[@class=" quote"]/text()')
        return "; ".join(examples)

    @staticmethod
    def get_sense_usage(sense_item: etree._Element):
        items = sense_item.xpath('./*[@class=" gramGrp"]')
        assert len(items) <= 1

        if len(items) == 0:
            return ""

        usage_item = items[0]

        text = ParentHtmlItem(usage_item).read()
        # found with a trailing space (' '), we must strip it:
        text = text.strip()
        assert(text[0] == "(")
        assert(text[-1] == ")")

        text = text[1: -1]
        return text

    @staticmethod
    def get_sense_categ(sense_item: etree._Element):
        items = sense_item.xpath('./*[@class=" lbl" and @type]')

        if len(items) == 0:
            return ""

        text_list = [ParentHtmlItem(usage_item).read() for usage_item in items]
        # we may have ' informal ' or the like.
        text = "".join(text_list).strip()

        return text

    def get_all_translations(self):
        items = self.root.xpath('//*[@class="translation_list clear"]/'
                                '*[@class="translation"]/'
                                '*[@class="hom lang_EN-GB"]')
        assert len(items) <= 1
        if len(items) == 0:
            return None

        sequence = items[0]

        word = sequence.xpath('./*[@class="inline"]/'
                              '*[@class="orth"]')
        assert len(word) == 1

        word_text = ParentHtmlItem(word[0]).read()

        neutral = sequence.xpath('./*[@class="neutral"]')
        assert len(neutral) == 3
        value_text = neutral[1].tail
        value_text = value_text.lower()

        item = neutral[2]

        def_text = ""
        assert isinstance(item, etree._Element)
        while not ("class" in item.keys() and item.get("class") == "example"):
            def_text += ParentHtmlItem(item).read()
            item = item.getnext()

        def_text = def_text.strip()

        ex_text = sequence.xpath('./*[@class="example"]/text()')[0]

        return [(word_text, value_text, def_text, ex_text)]


