from enum import Enum


class SearchIn(Enum):
    invalid = 0,
    definitions = 1
    examples = 2,
    all = 3


class ItemGatherer:
    def __init__(self):
        self.get_items = {
            SearchIn.definitions: ItemGatherer.gather_definitions,
            SearchIn.examples: ItemGatherer.gather_examples,
            SearchIn.all: ItemGatherer.gather_all
        }

    @staticmethod
    def gather_definitions(obj):
        return ItemGatherer._get_semantics(obj) + ItemGatherer._get_defs(obj) + ItemGatherer._get_translations(obj)

    @staticmethod
    def gather_examples(obj):
        return ItemGatherer._get_ex(obj) + ItemGatherer._get_translations(obj)

    @staticmethod
    def gather_all(obj):
        # return ItemGatherer._get_ex(obj) + ItemGatherer._get_translations(obj)
        raise NotImplementedError()

    @staticmethod
    def _get_semantics(obj: dict):
        return [x["semantics"] for x in obj["def_groups"] if "semantics" in x.keys()]

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

        for x in obj["def_groups"]:
            for ggroup in x["gram_groups"]:
                items += ItemGatherer._get_all_examples(ggroup["defs"])

        return items

    @staticmethod
    def _get_translations(obj: dict):
        items = []
        if "translations" in obj.keys():
            trans_list = ["[transl.] " + x for x in obj["translations"]]
            items += trans_list
        return items
