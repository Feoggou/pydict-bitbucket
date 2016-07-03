import os
import json

from src import config


class JsonLoader:
    @staticmethod
    def load(file_name: str):
        file_path = os.path.join(config.JSON_DIR_PATH, file_name)

        with open(file_path, "r", encoding="utf-8") as f:
            content = json.load(f)

        return content

