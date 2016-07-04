import re

from src.json_save import JsonSaver
from src.json_load import JsonLoader
from src.json_print import JsonPrinter
from src.content_retrieval import ContentRetrieval


def print_syn(word: str):
    printer = JsonPrinter()
    file_name = word + ".syn"

    content = JsonLoader().load(file_name)

    printer.print_syn(content)


def get_word(word: str):
    content_retrieval = ContentRetrieval()
    def_content, learn_content = content_retrieval.get_def_content(word)
    syn_content = content_retrieval.get_syn_content()
    saver = JsonSaver()

    saver.save(word + ".def", def_content)
    saver.save(word + ".learn", learn_content)
    saver.save(word + ".syn", syn_content)

    printer = JsonPrinter()
    printer.print(def_content)
    printer.print_learn(learn_content)


def process_input(input: str):
    matcher = re.match('syn\((.*)\)', input)
    if matcher:
        word = matcher.groups()[0]
        print_syn(word)
    else:
        get_word(input)
