from .json_save import JsonSaver
from .json_print import JsonPrinter
from .content_retrieval import ContentRetrieval


def process_input(input: str):
    content_retrieval = ContentRetrieval()

    def_content = content_retrieval.get_def_content()
    syn_content = content_retrieval.get_syn_content()

    saver = JsonSaver()
    saver.save("do.def", def_content)
    saver.save("do.syn", syn_content)

    printer = JsonPrinter()
    printer.print(def_content)


