#!/usr/bin/python3

import sys

sys.path.append("/home/zenith/PycharmProjects/EDictionary/v2")

from src.input_processor import process_input

input_text = input("dict> ")
process_input(input_text)
