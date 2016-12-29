import re
import os
import subprocess

from src import config
from src.json_load import JsonLoader
from src.json_save import JsonSaver
from src.json_print import JsonPrinter
from src.cmd_search import Search
from src.cmd_getword import get_word


def print_syn(word: str):
    printer = JsonPrinter()
    file_name = word + ".syn"

    content = JsonLoader().load(file_name)

    printer.print_syn(content)


def show_json(word: str):
    json_content = JsonLoader().load(word + ".def")
    json_str = JsonSaver().save_to_string(json_content)

    print(json_str)


def call_browser(word: str, browser: str):
    file_name = word
    if word.endswith("_defs") or word.endswith("_syn"):
        file_name += ".html"
    else:
        file_name += "_defs.html"
    file_path = os.path.join(config.HTML_SOURCE_PATH, file_name)
    subprocess.Popen([browser, file_path])


def call_firefox(word: str):
    call_browser(word, "firefox")


def call_chrome(word: str):
    call_browser(word, "/opt/google/chrome/chrome")


def output_text(results):
    print(results)


def call_search(expr: str):
    seeker = Search()
    results = seeker.search(expr)
    output_text(results)


def get_command_obj(cmd_name: str):
    switch = {
        "syn": print_syn,
        "search": call_search,
        "firefox": call_firefox,
        "chrome": call_chrome,
        "json": show_json,
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
