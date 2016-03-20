import json
import re
import os


def _get_all_defs(group):
    items = []

    for definition in group:
        if "def" in definition.keys():
            items.append(definition["def"])

        elif "def_subgroup" in definition.keys():
            items += _get_all_defs(definition["def_subgroup"])

    return items


def _get_all_examples(group):
    items = []

    for definition in group:
        if "example" in definition.keys():
            items.append(definition["example"])

        elif "def_subgroup" in definition.keys():
            items += _get_all_examples(definition["def_subgroup"])

    return items


class JsonSeeker:
    def __init__(self):
        pass

    def search_examples(self, word: str, dir_name: str) -> list:
        from os.path import isfile, join
        files = [x for x in os.listdir(dir_name) if isfile(join(dir_name, x))]

        results = []

        for file in files:
            file_name = join(dir_name, file)

            with open(file_name, "r") as json_file:
                obj = json.load(json_file)

                items = []
                for x in obj["def_groups"]:
                    for ggroup in x["gram_groups"]:
                        items += _get_all_examples(ggroup["defs"])

                pattern = re.compile(r'\b%s\b' % word)
                defs = [x for x in items if re.search(pattern, x)]
                if len(defs) > 0:
                    results.append({file: defs})

        return results

    def search_definitions(self, word: str, dir_name: str) -> list:
        from os.path import isfile, join
        files = [x for x in os.listdir(dir_name) if isfile(join(dir_name, x))]

        results = []

        for file in files:
            file_name = join(dir_name, file)

            with open(file_name, "r") as json_file:
                obj = json.load(json_file)

                items = []
                for x in obj["def_groups"]:
                    if "semantics" in x.keys():
                        items.append(x["semantics"])

                    for ggroup in x["gram_groups"]:
                        items += _get_all_defs(ggroup["defs"])

                pattern = re.compile(r'\b%s\b' % word)
                defs = [x for x in items if re.search(pattern, x)]
                if len(defs) > 0:
                    results.append({file: defs})

        return results

    def search_word_forms(self, word: str, dir_name: str) -> list:
        from os.path import isfile, join
        files = [x for x in os.listdir(dir_name) if isfile(join(dir_name, x))]

        results = []

        for file in files:
            file_name = join(dir_name, file)

            with open(file_name, "r") as json_file:
                obj = json.load(json_file)

                items = []
                for x in obj["def_groups"]:
                    items.append(x["word"])

                    if "derived_forms" in x.keys():
                        items += list(x["derived_forms"].values())

                    for ggroup in x["gram_groups"]:
                        if "word_forms" in ggroup.keys():
                            items += ggroup["word_forms"]

                if re.search('[\- \.\']', word):
                    defs = [x for x in items if word in x]
                    if len(defs) > 0:
                        results.append({file: defs})
                else:
                    pattern = re.compile(r'\b%s\b' % word)
                    defs = [x for x in items if re.search(pattern, x)]
                    if len(defs) > 0:
                        results.append({file: defs})

        return results
