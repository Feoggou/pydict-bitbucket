

def print_keys(elem, padding):
    keys_str = "({}) ".format(elem.tag)

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


def print_etree_elem(elem):
    if elem.tag is not None:
        print_elem(str(elem.tag), 0, "TAG")
    if elem.text is not None:
        print_elem(elem.text, 0, "TEXT")
    print_keys(elem, 0)
    # if e.keys() is not None:
#             print_elem(str(e.keys()), padding, "KEYS")
    if elem.tail is not None:
        print_elem(elem.tail, 0, "TAIL")


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


def print_summary(etree_elem):
    if etree_elem is None:
        print("ELEM: NULL!")
        return

    print_keys(etree_elem, 0)
    print("CHILDREN\n--------")

    # """
    for child_elem in etree_elem.getchildren():
        print_keys(child_elem, 0)
    # """
    # print_children(elem, 0)

