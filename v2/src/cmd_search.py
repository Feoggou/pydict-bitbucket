

class Search:
    def search(self, expr: str):
        self.find_files(expr)

    def find_files(self):
        raise NotImplementedError()
