def load_file(filename, folder="Lab1b") -> str:
    with open(f"../{folder}/{filename}") as file:
        file_content = file.read()

    return file_content


class TokensFile:
    def __init__(self):
        self.keywords = []
        self.keywords_identifier = {}
        self.operators = []
        self.operators_identifier = {}
        self.delimiters = []
        self.delimiters_identifier = {}
        self.separators = [" ", "\n"]
        self.startup_marker = "#BEGIN"
        self.end_marker = "#END"

        self._load_tokens()

    def _load_tokens(self):
        file_content = load_file("tokens.in").lower()
        self.keywords, self.keywords_identifier = self.parse_tokens("keywords", file_content, identifier_pos=3)
        self.operators, self.operators_identifier = self.parse_tokens("operators", file_content, identifier_pos=18)
        self.delimiters, self.delimiters_identifier = self.parse_tokens("delimiters", file_content, identifier_pos=34)

    @staticmethod
    def parse_tokens(token_name, file_content, identifier_pos=1):
        tokens = file_content.split(token_name)[1].split(']]')[0].split('[[')[1].strip()

        ret = []
        identifier, identifiers_list = identifier_pos, {}
        for token in tokens.split('---')[1:]:
            ret.append(token.strip())
            identifiers_list[token.strip()] = identifier
            identifier += 1

        return ret, identifiers_list

    def __str__(self):
        return f"Keywords: {self.keywords}\nOperators: {self.operators}\nDelimiters: {self.delimiters}"
