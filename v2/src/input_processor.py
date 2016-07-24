import re

from src.json_save import JsonSaver
from src.json_load import JsonLoader
from src.json_print import JsonPrinter
from src.content_retrieval import ContentRetrieval
from src.cmd_search import Search


def print_syn(word: str):
    printer = JsonPrinter()
    file_name = word + ".syn"

    content = JsonLoader().load(file_name)

    printer.print_syn(content)


def get_word(word: str):
    content_retrieval = ContentRetrieval()
    def_content, learn_content = content_retrieval.get_def_content(word)
    syn_content = content_retrieval.get_syn_content(word)
    saver = JsonSaver()

    saver.save(word + ".def", def_content)
    saver.save(word + ".learn", learn_content)
    saver.save(word + ".syn", syn_content)

    printer = JsonPrinter()
    printer.print(def_content)
    printer.print_learn(learn_content)


def output_text(text: str):
    print(text)


def call_search(expr: str):
    seeker = Search()
    results = seeker.search(expr)
    output_text(results)


def get_command_obj(cmd_name: str):
    switch = {
        "syn": print_syn,
        "search": call_search
    }

    cmd_obj = switch[cmd_name]
    if cmd_obj is None:
        raise ValueError("Unknown command: ", cmd_name)

    return cmd_obj


def process_input(input: str):
    matcher = re.match('([a-z]+)\((.*)\)', input)
    if matcher:
        cmd_name = matcher.groups()[0]
        arg = matcher.groups()[1]
        cmd = get_command_obj(cmd_name)
        cmd(arg)
    else:
        get_word(input)
