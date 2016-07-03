import re

from src.json_save import JsonSaver
from src.json_print import JsonPrinter
from src.content_retrieval import ContentRetrieval


def print_syn(word: str):
    printer = JsonPrinter()
    content = None
    printer.print_syn(content)


def process_input(input: str):
    matcher = re.match('syn\((.*)\)', input)
    if matcher:
        word = matcher.groups()[0]
        print_syn(word)
    else:
        content_retrieval = ContentRetrieval(from_web=False)

        def_content, learn_content = content_retrieval.get_def_content()
        syn_content = content_retrieval.get_syn_content()

        saver = JsonSaver()
        saver.save("do.def", def_content)
        saver.save("do.learn", learn_content)
        saver.save("do.syn", syn_content)

        printer = JsonPrinter()
        printer.print(def_content)

        printer.print_learn(learn_content)


