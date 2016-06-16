from lxml import etree
import re

IS_VERBOSE = False


def print_vb(*args):
    if IS_VERBOSE:
        print(args)


class HtmlItem:
    def __init__(self, etree_item: etree._Element, use_tail: bool=True, strip: bool=False):
        self.item = etree_item
        self.use_tail = use_tail
        self.strip = strip

        self.text = etree_item.text if etree_item.text is not None else ""
        self.tail = etree_item.tail if etree_item.tail is not None else ""

        print_vb("text: '{}'".format(self.text))
        print_vb("tail: '{}'".format(self.tail))

    def read(self):
        text = self.text

        if self.use_tail:
            text += self.tail

        if self.strip:
            text = text.strip()

        return text


class HtmlItemCreator:
    ALL_TAGS = None
    ALL_KEYS = None
    ALL_CLASSES = None

    def __init__(self):
        HtmlItemCreator.ALL_TAGS = {
            # "strong": HtmlItemCreator.create_default_item,
            "em": HtmlItemCreator.create_default_item,
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
            " xr": ParentHtmlItem,
            "xr_ref": ParentHtmlItem,  # XrRefItem,
            # "xr_ref_link": XrRefLinkItem,
            # "lbl register": ParentHtmlItem,  # LblRegisterItem,
            " lbl": ParentHtmlItem,
            # "orth": HtmlItemCreator.create_nothing,
            " orth": ParentHtmlItem,
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
    def __init__(self, etree_item: etree._Element, use_tail: bool=True, strip: bool=False):
        HtmlItem.__init__(self, etree_item)
        self.creator = HtmlItemCreator()
        self.use_tail = use_tail
        self.strip = strip

    def read(self):
        text = self.text
        text += self.read_children()
        if self.use_tail:
            text += self.tail

        text = re.sub(r' +', ' ', text)
        if self.strip:
            text = text.strip()

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