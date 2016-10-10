from src.content_retrieval import ContentRetrieval
from src.json_save import JsonSaver
from src.json_print import JsonPrinter


def get_word(word: str):
    content_retrieval = ContentRetrieval()
    def_content, learn_content, found = content_retrieval.get_def_content(word)

    if not found:
        saver = JsonSaver()

        saver.save(word + ".def", def_content)
        saver.save(word + ".learn", learn_content)

        try:
            syn_content = content_retrieval.get_syn_content(word)
            saver.save(word + ".syn", syn_content)
        except FileNotFoundError:
            print("Word '{}' has no synonyms.".format(word))

    printer = JsonPrinter()
    printer.print(def_content)
    printer.print_learn(learn_content)
