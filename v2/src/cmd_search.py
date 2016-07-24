import re

class Search:
    def search(self, expr: str):
        self.find_files(expr)

    def find_files(self, expr: str):
        file_names = self.collect_filenames(expr)

        return [x for x in file_names if self.file_name_matches(x, expr)]

    def collect_filenames(self, expr: str):
        raise NotImplementedError()

    @staticmethod
    def file_name_matches(file_name: str, what: str) -> bool:
        if not file_name.endswith(".def") and not file_name.endswith(".learn") and not file_name.endswith(".syn"):
            return False

        pattern = re.compile(r'\b{}\b'.format(what))
        return re.search(pattern, file_name)
