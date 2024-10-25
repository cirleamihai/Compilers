class LexicalParsingError(Exception):
    def __init__(self, file, line, token):
        self.file = file
        self.line = line
        self.token = token

    def __str__(self):
        return f"Lexical error in {self.file} at line {self.line}: {self.token}"
