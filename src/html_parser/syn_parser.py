from lxml import etree
import re


class SynParser:
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
            text = elem.text
            if len(elem.getchildren()) > 0:
                assert len(elem.getchildren()) == 1

                child = elem.getchildren()[0]
                assert(child.keys() == ["class"])
                assert child.get(child.keys()[0]) == "lbl register"

                child_text = child.text
                child_text += child.tail
                child_text = child_text.replace("\n", "")

                text += child_text

            return text

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
        homss = SynParser._get_all_home_subsecs(def_group)[0]

        elems = homss.xpath('./*[@class="hom"]')                                # 10 KEYS

        return elems

    @staticmethod
    def get_all_grammar_values(def_group):
        homss = SynParser._get_all_home_subsecs(def_group)[0]

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
    def get_syn_category(item: etree._Element):
        categs = []
        last_is_tail = False

        while item is not None and "class" in item.keys() and re.match("lbl .+", item.get("class")):
            last_is_tail = False
            """if item is None:
                return ""

            if "class" not in item.keys():
                return ""

            if not re.match("lbl .+", item.get("class")):
                return "" """

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
        """results = sense_list_item.xpath('./*[re:match(@class, "lbl .+")]',          # 13 KEYS or 15 KEYS
                             namespaces={"re": "http://exslt.org/regular-expressions"})"""

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

        """text_items = []
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
        text = text.replace("  ", " ")"""
        text = "".join(results)

        return text

