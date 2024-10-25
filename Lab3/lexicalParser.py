import re

from Lab3.tokensFile import *
from Lab3.lexicalErrors import *


class LexicalParser:
    def __init__(self, tokens: TokensFile, filename: str, folder: str):
        self.keywords = tokens.keywords
        self.operators = tokens.operators
        self.delimiters = tokens.delimiters
        self._startup_marker = tokens.startup_marker
        self._end_marker = tokens.end_marker
        self.identifier_pattern = re.compile(r'^[a-zA-Z][a-zA-Z0-9_]*$')  # identifier ::= letter { letter | digit | _ }
        self.line_count = 1
        self.filename = filename
        self.folder = folder

    def parse_file(self):
        program_content = load_file(self.filename, self.folder)
        file_content = program_content.split(self._startup_marker)[1].split(self._end_marker)[0]
        return self.parse(file_content)

    def parse(self, code):
        tokens = []
        buffer = ""
        i = 0

        while i < len(code):
            char = code[i]

            # Check for newline
            if char == '\n':
                self.line_count += 1  # Increment line count
                i += 1
                continue

            # Check for whitespace
            elif char.isspace():
                buffer = self.add_from_buffer(buffer, tokens)
                i += 1
                continue

            # Check for delimiters
            elif char in self.delimiters:
                buffer = self.add_from_buffer(buffer, tokens)
                tokens.append(("DELIMITER", char))
                i += 1

            # Check for operators
            elif char in self.operators:
                buffer = self.add_from_buffer(buffer, tokens)
                # Check for multi-character operators
                if i + 1 < len(code) and (char + code[i + 1]) in self.operators:
                    tokens.append(("OPERATOR", char + code[i + 1]))
                    i += 2
                else:
                    tokens.append(("OPERATOR", char))
                    i += 1

            # Accumulate characters for identifiers or constants
            else:
                buffer += char
                i += 1

        self.add_from_buffer(buffer, tokens)

        return tokens

    def add_from_buffer(self, buffer, tokens):
        if buffer:
            tokens.append(self.classify_token(buffer))

        return ""

    def classify_token(self, token):
        # Check for keywords
        if token in self.keywords:
            return "KEYWORD", token

        # Check for integer constants
        elif token.isdigit():
            return "CONSTANT", int(token)

        # Check for floating-point constants
        elif token.replace('.', '', 1).isdigit() and token.count('.') == 1:
            return "CONSTANT", float(token)

        # Check for string constants (single or double quotes)
        elif (token.startswith('"') and token.endswith('"')) or (token.startswith("'") and token.endswith("'")):
            return "CONSTANT", token.strip('"').strip("'")  # Strip quotes from the string value

        # Check for valid identifier
        elif self.identifier_pattern.match(token):
            return "IDENTIFIER", token

        # If none of the above, return an error for invalid identifier
        else:
            raise LexicalParsingError(file=self.filename, line=self.line_count, token=token)


