from src.json_save import JsonSaver
from src.json_print import JsonPrinter
from src.content_retrieval import ContentRetrieval


def process_input(input: str):
    content_retrieval = ContentRetrieval(from_web=False)

    def_content = content_retrieval.get_def_content()
    # TODO: syn content
    syn_content = content_retrieval.get_syn_content()

    saver = JsonSaver()
    saver.save("do.def", def_content)
    saver.save("do.syn", syn_content)

    printer = JsonPrinter()
    printer.print(def_content)


