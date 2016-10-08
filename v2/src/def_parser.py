from lxml import etree
import re

from src.html_item import *


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

        result = []
        for sequence in items:
            translation = self.get_one_translation(sequence)
            result.append(translation)

        return result

    @staticmethod
    def get_one_translation(sequence):
        word = sequence.xpath('./*[@class="inline"]/'
                              '*[@class="orth"]')

        assert len(word) == 1

        word_text = ParentHtmlItem(word[0]).read()

        categ_items = sequence.xpath('./span[@class="def"]')
        assert len(categ_items) <= 1

        categ_text = HtmlItem(categ_items[0]).read() if len(categ_items) else ""

        neutral = sequence.xpath('./*[@class="neutral"]')
        assert len(neutral) == 3

        value_text = neutral[1].tail
        value_text = value_text.lower()

        item = neutral[2]
        def_text = ""
        assert isinstance(item, etree._Element)

        while item is not None and \
                not ("class" in item.keys() and item.get("class") == "example"):
            def_text += ParentHtmlItem(item).read()
            item = item.getnext()

        def_text = def_text.strip()

        examples = sequence.xpath('./*[@class="example"]/text()')
        assert len(examples) <= 1

        ex_text = examples[0] if len(examples) else ""

        return {"word": word_text, "category": categ_text, "value": value_text, "def": def_text, "example": ex_text}

    @staticmethod
    def get_etymology(def_group: etree._Element):
        items = def_group.xpath('.//div[@class="content etyms"]/*[@class="hom_subsec etym"]')
        assert len(items) <= 1

        if len(items) == 0:
            items = def_group.xpath('.//div[@class="content etyms"]')
            assert len(items) <= 1

            if len(items) == 0:
                return ""

        # first child is "Word origin", but its tail is, e.g. "Old english" -- i.e. the first text elem in the sentence.
        etym_text = items[0].getchildren()[0].tail

        # first item is header, so we get from the second
        for item in items[0].getchildren()[1:]:
            text = HtmlItem(item).read()
            etym_text += text

        return etym_text

    @staticmethod
    def get_derived_forms(def_group: etree._Element):
        items = def_group.xpath('.//div[@class="content derivs"]/*[@class="hom_subsec re"]')
        assert len(items) <= 1

        if len(items) == 0:
            return "", ""

        form_items = items[0].xpath('./span[@class=" form"]/span[@class=" orth"]')
        if len(form_items) == 0:
            form_items = items[0].xpath('./span[@class=" form"]')
        assert len(form_items) == 1
        form_text = ParentHtmlItem(form_items[0], strip=True).read()
        form_text = form_text.replace("ˈ", "")

        gram_items = items[0].xpath('./span[@class=" hom"]')
        assert len(gram_items) == 1
        gram_text = ParentHtmlItem(gram_items[0], strip=True).read()

        return form_text, gram_text
