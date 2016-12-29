import unittest
from unittest import mock
from unittest.mock import patch

from src.json_collector import JsonCollector, DefCollector

def_conent_word_forms = {
    "def_groups": [
        {
            "derived_forms": {
                "doable": "noun",
                "undoable": "noun"
            },
            "word": "do",
            "origin": "dummy",
            "frequency": "dummy",
            "gram_groups": [
                {
                    "forms": {"items": ["does", "doing", "did", "done"], "info": ""},
                    "value": "dummy",
                    "defs": {}
                },
                {
                    "forms": {"items": ["dos", "do's"], "info": "plural"},
                    "value": "dummy",
                    "defs": {}
                }
            ]
        },
        {
            "word": "do or do a",
            "gram_groups": [{"forms": {"items": [], "info": ""}, "defs": {}}]
        },
        {
            "word": "do",
            "gram_groups": [{"forms": {"items": ["dos"], "info": "plural"}}]
        },
        {"word": "DO"},
        {"word": "do."}
    ]
}

learn_content_word_forms = [
    {
        "forms": ["taller", "tallest"],
        "gram_groups": [],
        "word": "tall"
    },
    {
        "word": "do - auxiliary verb uses",
        "forms": ["does", "doing", "did", "done"],
        "gram_groups": []
    },
    {
        "word": "do.",
        "forms": [],
        "gram_groups": []
    }
]


class TestJsonCollector(unittest.TestCase):
    def test_collectWordForms_def_callsDefCollect(self):
        collector = JsonCollector()
        content = {"dummy": "content"}

        with patch.object(DefCollector, "collect_word_forms") as mock_collect:
            collector.collect_word_forms("def", content)

        mock_collect.assert_called_once_with(content)

    def test_def_collectWordForms(self):
        collector = DefCollector()

        result = collector.collect_word_forms(def_conent_word_forms)

        self.assertEqual([
            "DO", "did", "do", "do or do a", "do's", "do.", "doable", "does", "doing", "done", "dos", "undoable"
        ], result)

    def test_collectWordForms_requestsLearn(self):
        collector = JsonCollector()

        result = collector.collect_word_forms("learn", learn_content_word_forms)

        self.assertEqual([
            "did", "do - auxiliary verb uses", "do.", "does", "doing",  "done", "tall", "taller", "tallest",
        ], result)


if __name__ == '__main__':
    unittest.main()
