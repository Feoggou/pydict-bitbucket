# from lxml.html import tostring, fromstring

def print_elem(elem_text, padding, name):
    text=""
    if not elem_text:
        text=None
    if elem_text and not elem_text.isspace():
        text=elem_text
    else:
        text="((space))"

    if text:
        print('{:2} {}:{} "{}"'.format(padding // 4, name, " " * padding, text))


def print_keys(elem, padding):
    keys_str = ""

    for k in elem.keys():
        keys_str += '{}="{}"; '.format(k, elem.get(k))

    text=""
    if not keys_str:
        text=None
    elif keys_str and not keys_str.isspace():
        assert(len(keys_str) > 1)
        text=keys_str
    else:
        text="((space))"

    if text is not None:
        print('{:2} KEYS:{} {}'.format(padding // 4, " " * padding, text))


def print_children(elem, padding):
    assert(elem is not None)

    for e in elem.getchildren():
        assert(e is not None)

        if e.tag is not None:
            print_elem(str(e.tag), padding, "TAG")
        if e.text is not None:
            print_elem(e.text, padding, "TEXT")
        print_keys(e, padding)
        # if e.keys() is not None:
#             print_elem(str(e.keys()), padding, "KEYS")
        if e.tail is not None:
            print_elem(e.tail, padding, "TAIL")

        print("\n")
        print_children(e, padding + 4)

################################################

# key: class="definitions hom-subsec"
#   key: class="h2_entry"
#       key: class="pos" --- i.e. grammar value (e.g. noun)
#       key: class="inflected_forms" --- has word forms
#       key: class="sense_list level_<n>"; value="n"; ---- 1.a, 1.b, 2.a, etc.
#          key: class="def"     --- word definition
#               key: class="hi"     --- word example (in 'class="orth"' --- there may be many)


class DictElem:

    # elems = [HomeElem, BaseValue, GrammarValue, WordForms, SenseList, DefinitionElem, BaseExamples, WordExample]
    # key = ()

    def create_dict_elem(key):
        for e in DictElem.elems:
            assert isinstance(e, DictElem)
            if e.key == key:
                return e()


    def __init__(self):
        self.text = ""
        self.children = []

    def has_child(self, key):
        for child_key in self.children:
            # assert isinstance(child, BaseValue)
            if child_key == key:
                return child_key
            return None

    def add_child(self, elem):
        key_name = elem.keys()[0]
        key = key_name, elem.get(key_name)

        for child_key in self.children:
            if child_key == key:
                pass




    def fetch_data(self, elem):
        pass


class HomeElem(DictElem):
    key = ('class', 'definitions hom-subsec')
    children_keys = [BaseValue.key]

    def __init__(self):
        print("HomeElem")


class BaseValue(DictElem):
    key = ('class', 'h2_entry')
    children_keys = [GrammarValue.key, WordForms.key, SenseList.key]

    def __init__(self):
        print("BaseValue")


class GrammarValue(DictElem):
    key = ('class', 'pos')
    children_keys = []

    def __init__(self):
        print("GrammarValue")


class WordForms(DictElem):
    key = ('class', 'inflected_forms')
    children_keys = []

    def __init__(self):
        print("WordForms")


class SenseList(DictElem):
    key = ('class', 'sense_list level_1')
    children_keys = [DefinitionElem.key]
    names = [('class', 'sense_list level_'), ('value', '')]

    def __init__(self):
        print("SenseList")


class DefinitionElem(DictElem):
    key = ('class', 'def')
    children_keys = [BaseExamples.key]

    def __init__(self):
        print("DefinitionElem")


class BaseExamples(DictElem):
    key = ('class', 'orth')
    children_keys = [WordExample.key]

    def __init__(self):
        print("BaseExamples")


class WordExample(DictElem):
    key = ('class', 'hi')
    children_keys = []

    def __init__(self):
        print("BaseExamples")


def traverse_children(text_elem, item):
    assert(text_elem is not None)

    for e in text_elem.getchildren():
        assert(e is not None)

        keys = e.keys()
        assert isinstance(keys, list)

        if len(keys) > 0:
            first_key = keys[0]
            if item is None:
                if first_key == 'class' and e.get(first_key) == 'definitions hom-subsec':
                    print_keys(e, 4)
                    item = HomeElem()

            else:
                assert isinstance(item, DictElem)

                key = first_key, e.get(first_key)
                if item.has_child(key):
                    item.add_child(e)
                    item = child
                    # print_keys(e, 4)
                    # if item.text is not None:
                    #     print('\t\t\t"{}"'.format(item.text))
                    # item.fetch_data(e)
        # e.tag
        # e.text
        # e.keys()
        # e.tail

        traverse_children(e, item)