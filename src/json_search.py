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


def _get_all_categs(group):
    items = []

    for definition in group:
        if "def" in definition.keys():
            categ = ""
            if "category" in definition.keys():
                categ = "({}) ".format(definition["category"])

            item = categ + definition["def"]
            if "example" in definition.keys():
                item = item + "\n    e.g." + definition["example"]
            items.append(item)

        elif "def_subgroup" in definition.keys():
            categ = ""
            if "category" in definition.keys():
                categ = "({}) ".format(definition["category"])

            subdefs = _get_all_categs(definition["def_subgroup"])

            subdefs_changed = []
            for subdef in subdefs:
                subdef = categ + subdef
                subdefs_changed.append(subdef)

            items += subdefs_changed

        else:
            if "category" in definition.keys():
                item = "({}) (for synonym)".format(definition["category"])
                items.append(item)

    return items


def _get_all_examples(group):
    items = []

    for definition in group:
        if "example" in definition.keys():
            items.append(definition["example"])

        elif "def_subgroup" in definition.keys():
            items += _get_all_examples(definition["def_subgroup"])

    return items


def print_list(value: list):
    for x in value:
        file = list(x)[0]
        print("[" + file + "]")
        for definition in x[file]:
            print("o) " + definition)

        print("")


def find_word_in_list_loose(word: str, items: list) -> list:
    # lowercase does not matter, word can be " " or "-"
    lower_word = word.lower()

    if re.search('[\- \.\']', lower_word):
        defs = [x for x in items if lower_word in (x.replace(" ", "-").lower())]
    else:
        pattern = re.compile(r'\b%s\b' % lower_word)
        defs = [x for x in items if re.search(pattern, x.lower())]

    return defs


def find_word_in_list_exact(word: str, items: list) -> list:
    # i.e. matters lowercase, and must be whole word (without " " or "-")
    pattern = re.compile(r'\b%s\b' % word)
    defs = [x for x in items if re.search(pattern, x)]

    return defs


def find_word_in_list_exact_extended(word: str, items: list) -> list:
    # i.e. matters lowercase and whether we have " " or "-"
    if re.search('[\- \.\']', word):
        defs = [x for x in items if word in x]
    else:
        pattern = re.compile(r'\b%s\b' % word)
        defs = [x for x in items if re.search(pattern, x)]

    return defs


class JsonSeeker:
    def __init__(self):
        # search_categories
        pass

    @staticmethod
    def search_categories(word: str, dir_name: str) -> list:
        from os.path import isfile, join
        files = [x for x in os.listdir(dir_name) if isfile(join(dir_name, x))]
        files = [x for x in files if ".json" in x]

        results = []

        for file in files:
            file_name = join(dir_name, file)

            with open(file_name, "r") as json_file:
                obj = json.load(json_file)

                items = []
                for x in obj["def_groups"]:
                    for ggroup in x["gram_groups"]:
                        items += _get_all_categs(ggroup["defs"])

                if "synonyms" in obj.keys():
                    for x in obj["synonyms"]:
                        for ggroup in x["gram_groups"]:
                            items += _get_all_categs(ggroup["gram_group"]["synonyms"])

                items = sorted(list(set(items)))

                defs = find_word_in_list_loose(word, items)
                if len(defs) > 0:
                    results.append({file: defs})

        return results

    @staticmethod
    def search_examples(word: str, dir_name: str, translations=True) -> list:
        from os.path import isfile, join
        files = [x for x in os.listdir(dir_name) if isfile(join(dir_name, x))]
        files = [x for x in files if ".json" in x]

        results = []

        for file in files:
            file_name = join(dir_name, file)

            with open(file_name, "r") as json_file:
                obj = json.load(json_file)

                items = []
                for x in obj["def_groups"]:
                    for ggroup in x["gram_groups"]:
                        items += _get_all_examples(ggroup["defs"])

                if translations and "translations" in obj.keys():
                    trans_list = ["[transl.] " + x for x in obj["translations"]]
                    items += trans_list

                items = sorted(list(set(items)), reverse=True)

                defs = find_word_in_list_loose(word, items)
                if len(defs) > 0:
                    results.append({file: defs})

        return results

    @staticmethod
    def search_definitions(word: str, dir_name: str, translations=True) -> list:
        from os.path import isfile, join
        files = [x for x in os.listdir(dir_name) if isfile(join(dir_name, x))]
        files = [x for x in files if ".json" in x]

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

                if translations and "translations" in obj.keys():
                    trans_list = ["[transl.] " + x for x in obj["translations"]]
                    items += trans_list

                items = sorted(list(set(items)), reverse=True)

                defs = find_word_in_list_exact(word, items)
                if len(defs) > 0:
                    results.append({file: defs})

        return results

    @staticmethod
    def search_translations(word: str, dir_name: str) -> list:
        from os.path import isfile, join
        files = [x for x in os.listdir(dir_name) if isfile(join(dir_name, x))]
        files = [x for x in files if ".json" in x]

        results = []

        for file in files:
            file_name = join(dir_name, file)

            with open(file_name, "r") as json_file:
                obj = json.load(json_file)

                items = []
                if "translations" in obj.keys():
                    items += obj["translations"]

                items = sorted(list(set(items)))

                defs = find_word_in_list_exact(word, items)
                if len(defs) > 0:
                    results.append({file: defs})

        return results

    @staticmethod
    def search_word_forms(word: str, dir_name: str) -> list:
        from os.path import isfile, join
        files = [x for x in os.listdir(dir_name) if isfile(join(dir_name, x))]
        files = [x for x in files if ".json" in x]

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

                items = sorted(list(set(items)))

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

    @staticmethod
    def search_synonyms(word: str, dir_name: str) -> list:
        from os.path import isfile, join
        files = [x for x in os.listdir(dir_name) if isfile(join(dir_name, x))]
        files = [x for x in files if ".json" in x]

        results = []

        for file in files:
            file_name = join(dir_name, file)

            with open(file_name, "r") as json_file:
                obj = json.load(json_file)

                items = []

                if "synonyms" not in obj.keys():
                    continue

                for x in obj["synonyms"]:
                    items.append(x["word"])

                    for ggroup in x["gram_groups"]:
                        syns_obj = ggroup["gram_group"]
                        for line in syns_obj["synonyms"]:
                            items += line["line"]

                items = sorted(list(set(items)))

                defs = find_word_in_list_loose(word, items)
                if len(defs) > 0:
                        results.append({file: defs})

        return results

    @staticmethod
    def search_related(word: str, dir_name: str) -> list:
        from os.path import isfile, join
        files = [x for x in os.listdir(dir_name) if isfile(join(dir_name, x))]
        files = [x for x in files if ".json" in x]

        results = []

        for file in files:
            file_name = join(dir_name, file)

            with open(file_name, "r") as json_file:
                obj = json.load(json_file)

                items = []

                if "related_words" in obj.keys():
                    items += obj["related_words"]

                for def_group in obj["def_groups"]:
                    if "related" in def_group.keys():
                        items += def_group["related"]

                if "nearby_words" in obj.keys():
                    items += obj["nearby_words"]

                items = sorted(list(set(items)))

                defs = find_word_in_list_loose(word, items)
                if len(defs) > 0:
                        results.append({file: defs})

        return results

    @staticmethod
    def search_all(word: str, dir_name: str) -> list:
        # P0: files with the name "<word>.json"
        from os.path import isfile, join

        files = [x.replace(".json", "") for x in os.listdir(dir_name) if isfile(join(dir_name, x)) and ".json" in x]
        if word in files:
            print("=== FILES ===")
            print(word + ".json\n")

        # P1. word forms (and derived forms)
        word_forms = JsonSeeker.search_word_forms(word, dir_name)
        if len(word_forms):
            print("=== WORD FORMS ===")
            print_list(word_forms)

        # P2. synonyms
        synonyms = JsonSeeker.search_synonyms(word, dir_name)
        if len(synonyms):
            print("=== SYNONYMS ===")
            print_list(synonyms)

        # P3. related & nearby
        related = JsonSeeker.search_related(word, dir_name)
        if len(related):
            print("=== RELATED / NEARBY ===")
            print_list(related)

        # P4. definitions & semantics
        definitions = JsonSeeker.search_definitions(word, dir_name, translations=False)
        if len(definitions):
            print("=== DEFINITIONS ===")
            print_list(definitions)

        # P5. examples
        examples = JsonSeeker.search_examples(word, dir_name, translations=False)
        if len(examples):
            print("=== EXAMPLES ===")
            print_list(examples)

        # P6. translations
        translations = JsonSeeker.search_translations(word, dir_name)
        if len(definitions):
            print("=== TRANSLATIONS ===")
            print_list(translations)

        # P7. categories
        categories = JsonSeeker.search_categories(word, dir_name)
        if len(categories):
            print("=== CATEGORIES ===")
            print_list(categories)
