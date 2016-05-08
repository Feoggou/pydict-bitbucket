from enum import Enum


class SearchIn(Enum):
    invalid = 0,
    definitions = 1,
    examples = 2,
    word_forms = 3,
    synonyms = 4,
    related = 5,
    definitions_simple = 6,
    examples_simple = 7,
    semantics = 8,
    translations = 9,
    categories = 10,


class ItemGatherer:
    def __init__(self):
        self.get_items = {
            SearchIn.definitions: ItemGatherer.gather_definitions,
            SearchIn.examples: ItemGatherer.gather_examples,
            SearchIn.word_forms: ItemGatherer.gather_word_forms,
            SearchIn.synonyms: ItemGatherer.gather_synonyms,
            SearchIn.related: ItemGatherer.gather_related,
            SearchIn.definitions_simple: ItemGatherer.gather_definitions_simple,
            SearchIn.examples_simple: ItemGatherer.gather_examples_simple,
            SearchIn.semantics: ItemGatherer.gather_semantics,
            SearchIn.translations: ItemGatherer.gather_translations,
            SearchIn.categories: ItemGatherer.gather_categories,
        }

    @staticmethod
    def gather_categories(obj):
        return ItemGatherer._get_categories(obj)

    @staticmethod
    def gather_definitions(obj):
        return ItemGatherer._get_semantics(obj) + ItemGatherer._get_defs(obj) + ItemGatherer._get_translations(obj)

    @staticmethod
    def gather_definitions_simple(obj):
        return ItemGatherer._get_defs(obj)

    @staticmethod
    def gather_examples(obj):
        return ItemGatherer._get_ex(obj) + ItemGatherer._get_translations(obj)

    @staticmethod
    def gather_examples_simple(obj):
        return ItemGatherer._get_ex(obj)

    @staticmethod
    def gather_semantics(obj):
        return ItemGatherer._get_semantics(obj)

    @staticmethod
    def gather_translations(obj):
        return ItemGatherer._get_translations(obj, mark=False)

    @staticmethod
    def gather_word_forms(obj):
        return ItemGatherer._get_words(obj) + ItemGatherer._get_derived_forms(obj) + ItemGatherer._get_word_forms(obj)

    @staticmethod
    def gather_synonyms(obj):
        items = []

        if "synonyms" not in obj.keys():
            return []

        for x in obj["synonyms"]:
            # items.append(x["word"])

            for ggroup in x["gram_groups"]:
                syns_obj = ggroup["gram_group"]
                for line in syns_obj["synonyms"]:
                    items += [x["syn"] for x in line["line"]]

        return items

    @staticmethod
    def gather_related(obj):
        items = []

        if "related_words" in obj.keys():
            items += obj["related_words"]

        for def_group in obj["def_groups"]:
            if "related" in def_group.keys():
                items += def_group["related"]

        if "nearby_words" in obj.keys():
            items += obj["nearby_words"]

        return items

    @staticmethod
    def _get_categories(obj: dict):
        items = []
        for x in obj["def_groups"]:
            for ggroup in x["gram_groups"]:
                items += ItemGatherer._get_all_categs(ggroup["defs"])

        if "synonyms" in obj.keys():
            for x in obj["synonyms"]:
                for ggroup in x["gram_groups"]:
                    items += ItemGatherer._get_all_categs(ggroup["gram_group"]["synonyms"])

        return items

    @staticmethod
    def _get_semantics(obj: dict):
        return [x["semantics"] for x in obj["def_groups"] if "semantics" in x.keys()]

    @staticmethod
    def _get_words(obj: dict):
        items = [x["word"] for x in obj["def_groups"]]

        return items

    @staticmethod
    def _get_derived_forms(obj: dict):
        items = []

        for x in obj["def_groups"]:
            if "derived_forms" in x.keys():
                items += list(x["derived_forms"].values())

        return items

    @staticmethod
    def _get_word_forms(obj: dict):
        items = []

        for x in obj["def_groups"]:
            for ggroup in x["gram_groups"]:
                if "word_forms" in ggroup.keys():
                    items += ggroup["word_forms"]

        return items

    @staticmethod
    def _get_all_defs(group):
        items = []

        for definition in group:
            if "def" in definition.keys():
                items.append(definition["def"])

            elif "def_subgroup" in definition.keys():
                items += ItemGatherer._get_all_defs(definition["def_subgroup"])

        return items

    @staticmethod
    def _get_all_examples(group):
        items = []

        for definition in group:
            if "example" in definition.keys():
                items.append(definition["example"])

            elif "def_subgroup" in definition.keys():
                items += ItemGatherer._get_all_examples(definition["def_subgroup"])

        return items

    @staticmethod
    def _get_defs(obj: dict):
        items = []

        for x in obj["def_groups"]:
            for ggroup in x["gram_groups"]:
                items += ItemGatherer._get_all_defs(ggroup["defs"])

        return items

    @staticmethod
    def _get_ex(obj: dict):
        items = []

        for x in obj["examples"]:
            items.append(x["example"])

        if "my_examples" in obj:
            for x in obj["my_examples"]:
                items.append(x["example"])

        for x in obj["def_groups"]:
            for ggroup in x["gram_groups"]:
                items += ItemGatherer._get_all_examples(ggroup["defs"])

        return items

    @staticmethod
    def _get_translations(obj: dict, mark: bool = True):
        items = []
        if "translations" in obj.keys():
            if mark:
                trans_list = ["[transl.] " + x for x in obj["translations"]]
            else:
                trans_list = [x for x in obj["translations"]]
            items += trans_list
        return items

    @staticmethod
    def _get_all_categs(group):
        items = []

        for definition in group:
            if "def" in definition.keys():
                if "category" in definition.keys():
                    items.append(definition["category"])

            elif "def_subgroup" in definition.keys():
                if "category" in definition.keys():
                    items.append(definition["category"])

                items += ItemGatherer._get_all_categs(definition["def_subgroup"])

            else:
                if "category" in definition.keys():
                    items.append(definition["category"])

                for syn in definition["line"]:
                    if "category" in syn.keys():
                        items.append(syn["category"])

        return items
