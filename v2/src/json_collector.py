

class JsonCollector:
    def collect_word_forms(self, file_kind: str, content):
        collectors = {
            "def": DefCollector,
            "learn": LearnCollector,
            "syn": SynCollector
            }
        collector = collectors.get(file_kind, None)
        if collector is None:
            raise RuntimeError("Could not find collector for: " + file_kind)

        return collector().collect_word_forms(content)


class DefCollector:
    def collect_word_forms(self, content: dict):
        results = []

        for def_group in content["def_groups"]:
            results += self._collect_wordforms_from_defgroup(def_group)

        return sorted(list(set(results)))

    def _collect_wordforms_from_defgroup(self, def_group):
        results = []

        word = def_group["word"]
        results.append(word)

        derived_forms = def_group.get("derived_forms", {})
        results += derived_forms.keys()

        results += self._collect_wordforms_from_ggroups(def_group)
        return results

    @staticmethod
    def _collect_wordforms_from_ggroups(def_group):
        results = []

        if "gram_groups" not in def_group:
            return []

        for ggroup in def_group["gram_groups"]:
            forms = ggroup.get("forms", {})
            if len(forms):
                word_forms = forms["items"]
                results += word_forms

        return results


class LearnCollector:
    def collect_word_forms(self, content: list):
        results = []

        for group in content:
            word = group["word"]
            results.append(word)

            forms = group["forms"]
            results += forms

        return sorted(list(set(results)))


class SynCollector:
    def collect_word_forms(self, content: list):
        return []
