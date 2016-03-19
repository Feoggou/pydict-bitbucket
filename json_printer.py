import json

tab = "    "


def read_definition(definition, indent: int = 0) -> str:
    if "def_subgroup" in definition.keys():
        s = ""
        if "category" in definition.keys():
            s += "({}) ".format(definition["category"])
        s = "{}o) {}\n".format(tab * indent, s)
        for subdef in definition["def_subgroup"]:
            s += read_definition(subdef, indent + 1)
    else:
        s = definition["def"]
        if "example" in definition.keys():
            s += "\n{}e.g. {}".format(tab * (indent + 1), definition["example"])
        if "category" in definition.keys():
            s = "({}) {}".format(definition["category"], s)

        s = (tab * indent) + ("o) " if indent == 0 else " ") + s
        s += "\n"

    return s


def read_gram_group(gram_group) -> str:
    s = ""
    if "value" in gram_group.keys():
        s += gram_group["value"] + "\n"

    for definition in gram_group["defs"]:
        s += read_definition(definition)

    s += "\n"
    return s


def read_gram_groups(gram_groups) -> str:
    s = gram_groups["word"] + "\n"
    for gram_group in gram_groups["gram_groups"]:
        s += read_gram_group(gram_group)

    return s


def read_def_groups(obj) -> str:
    s = "DEFINTIONS\n"
    for gram_groups in obj["def_groups"]:
        s += read_gram_groups(gram_groups)

    s += "\n"
    return s


def read_examples(obj) -> str:
    s = "EXAMPLES\n"
    for example in obj["examples"]:
        s += "o) " + example["example"] + "\n"

    s += "\n"
    return s


def read_frequency(obj) -> str:
    return "[{}]\n\n".format(obj["frequency"])


def read_syn_lines(syns_obj) -> str:
    s = ""
    for line in syns_obj["synonyms"]:
        string = "o) "
        if "category" in line.keys():
            string += "({}) ".format(line["category"])
        string += ", ".join(line["line"])
        s += string + "\n"
    return s


def read_syn_gram_group(ggroup) -> str:
    s = ggroup["gram_group"]["value"] + "\n"
    s += read_syn_lines(ggroup["gram_group"])
    s += "\n"
    return s


def read_syn_def_group(syn_obj) -> str:
    s = syn_obj["word"] + "\n"
    for gram_group in syn_obj["gram_groups"]:
        s += read_syn_gram_group(gram_group)
    return s


def read_synonyms(obj: dict) -> str:
    s = "SYNONYMS\n"
    if "synonyms" not in obj.keys():
        return ""

    for syn_obj in obj["synonyms"]:
        s += read_syn_def_group(syn_obj)
    s += "\n"
    return s

# HERE WE HAVE THE ACTUAL CALLING CODE


class JsonPrinter:
    def __init__(self):
        pass

    def to_text(self, json_file_name: str):
        with open(json_file_name, "r") as json_file:
            obj = json.load(json_file)
            s = read_frequency(obj)
            s += read_def_groups(obj)
            s += read_synonyms(obj)
            s += read_examples(obj)

            return s

