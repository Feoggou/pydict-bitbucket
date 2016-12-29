#!/usr/bin/python3

import sys
from src import config

sys.path.append(config.PROJECT_PATH)

from src.input_processor import process_input

input_text = input("dict> ")
process_input(input_text)
