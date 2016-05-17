from lxml import etree
import re


class HtmlParser:
    def __init__(self, root, word_name):
        self.root = root
        self.word_name = word_name
        assert isinstance(self.root, etree._Element)

        self.main_elem = self.root.xpath('//*[@class="definition_main"]')[0]    # 5 KEYS
        assert isinstance(self.main_elem, etree._Element)

        self.mainbar_elem = self.main_elem.xpath('//*[@class="definition_content col main_bar"]')[0]    # 6 KEYS

        assert isinstance(self.mainbar_elem, etree._Element)

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
            # TODO: Syn has different here. Is the syn version better?
            return elem.text

    def _get_homsubsec_name(self):
        raise NotImplementedError()

    def get_all_home_subsecs(self, def_group):
        elems = def_group.xpath('./*[@class="homograph-entry"]/'              # 8 KEYS
                           '*[@class="{} hom-subsec"]'
                                .format(self._get_homsubsec_name()))    # 9 KEYS

        return elems

    def _get_gramgroup_name(self):
        raise NotImplementedError()

    def get_all_grammar_groups(self, def_group):
        homss = self.get_all_home_subsecs(def_group)[0]

        elems = homss.xpath('./*[@class="hom"]')                                # 10 KEYS

        return elems

    def get_all_grammar_values(self, def_group):
        homss = self.get_all_home_subsecs(def_group)[0]

        elems = homss.xpath('./*[@class="hom"]/'                                # 10 KEYS
                            '*[@class="{}"]/'                                   # 11 KEYS
                            '*[@class="pos"]'
                            .format(self._get_gramgroup_name()))          # 12 KEYS

        result = [elem.text for elem in elems]
        return result

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
                text += subelement + item.tail
            elif "class" in item.keys() and item.get("class") == "hi":
                if item.text is not None:
                    text += item.text
                if item.tail is not None:
                    text += item.tail

        text = re.sub(' +', ' ', text)
        text = text.replace("\n", "")
        return text

    def get_gram_value(self, gram_group):
        elems = gram_group.xpath('./*[@class="{}"]/'                   # 11 KEYS
                                '*[@class="pos"]'
                                 .format(self._get_gramgroup_name()))                               # 12 KEYS

        if len(elems):
            text = " ".join([x.text for x in elems if len(x.text) > 0])
            return text

        return ""

    @staticmethod
    def get_word_forms(ggroup):
        elems = ggroup.xpath('./*[@class="inflected_forms"]/'                 # 11 KEYS
                             '*[@class="infl"]')                              # 12 KEYS

        result = []
        for e in elems:
            # t = e.text.replace("ˈ", "'")
            t = e.text.replace("ˈ", "").replace("ˌ", "")
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

        # TODO SYN ----
        if len(results) == 0:
            results = sslist_etree.xpath('./*[re:match(@class, "sense_list_item level_\d")]',  # 11 KEYS or 13 KEYS
                                         namespaces={"re": "http://exslt.org/regular-expressions"})
            assert (len(results) == 1)
            assert "value" not in results[0].keys()
            # ---- SYN

        elem = results[0]

        return elem

    @staticmethod
    def get_all_senselist_items(sslist_etree):
        results = sslist_etree.xpath('./*[re:match(@class, "sense_list_item level_\d")]', # 11 KEYS or 13 KEYS
                             namespaces={"re": "http://exslt.org/regular-expressions"})

        return results

