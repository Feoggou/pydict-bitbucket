from lxml import etree


class RelatedParser:
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

