
RESET = "\033[0m"
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

BOLDBLACK = "\033[1m\033[30m"
BOLDRED = "\033[1m\033[31m"
BOLDGREEN = "\033[1m\033[32m"
BOLDYELLOW = "\033[1m\033[33m"
BOLDBLUE = "\033[1m\033[34m"
BOLDMAGENTA = "\033[1m\033[35m"
BOLDCYAN = "\033[1m\033[36m"
BOLDWHITE = "\033[1m\033[37m"


class ColoredText:
    reset_color = ""
    title_color = ""
    h1_color = ""
    word_color = ""
    gram_color = ""
    usage_color = ""

    @staticmethod
    def init_values():
        ColoredText.reset_color = RESET
        ColoredText.title_color = RED
        ColoredText.h1_color = BLUE
        ColoredText.word_color = BOLDBLACK
        ColoredText.gram_color = RED
        ColoredText.usage_color = GREEN

    @staticmethod
    def colored_title(s: str):
        return ColoredText.title_color + s + ColoredText.reset_color

    @staticmethod
    def colored_h1(s: str):
        return ColoredText.h1_color + s + ColoredText.reset_color

    @staticmethod
    def colored_word(s: str):
        return ColoredText.word_color + s + ColoredText.reset_color

    @staticmethod
    def colored_gram(s: str):
        return ColoredText.gram_color + s + ColoredText.reset_color

    @staticmethod
    def colored_usage(s: str):
        return ColoredText.usage_color + s + ColoredText.reset_color
