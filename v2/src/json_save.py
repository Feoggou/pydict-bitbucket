import os
import json

from src import config


class JsonSaver:
    @staticmethod
    def save(file_name: str, content):
        file_path = os.path.join(config.JSON_DIR_PATH, file_name)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(content, f, indent=4, sort_keys=True, ensure_ascii=False)

