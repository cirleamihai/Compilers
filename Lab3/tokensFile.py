def load_file(filename, folder="Lab1b") -> str:
    with open(f"../{folder}/{filename}") as file:
        file_content = file.read()

    return file_content


class TokensFile:
    def __init__(self):
        self.keywords = []
        self.operators = []
        self.delimiters = []
        self.separators = [" ", "\n"]
        self.startup_marker = "#BEGIN"
        self.end_marker = "#END"

        self._load_tokens()

    def _load_tokens(self):
        file_content = load_file("tokens.in").lower()
        self.keywords = self.parse_tokens("keywords", file_content)
        self.operators = self.parse_tokens("operators", file_content)
        self.delimiters = self.parse_tokens("delimiters", file_content)

    @staticmethod
    def parse_tokens(token_name, file_content):
        tokens = file_content.split(token_name)[1].split(']]')[0].split('[[')[1].strip()

        ret = []
        for token in tokens.split('---')[1:]:
            ret.append(token.strip())
        return ret

    def __str__(self):
        return f"Keywords: {self.keywords}\nOperators: {self.operators}\nDelimiters: {self.delimiters}"
