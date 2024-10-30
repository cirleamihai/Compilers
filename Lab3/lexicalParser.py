import re

from Lab3.tokensFile import *
from Lab3.lexicalErrors import *


def _looks_like_string(token):
    return token == '"' or token == "'" or (
                (token.startswith('"') or token.startswith("'"))
                and not (token.endswith('"') or token.endswith("'")))


def _is_string(token):
    return (token.startswith('"') and token.endswith('"')) or (token.startswith("'") and token.endswith("'"))


class LexicalParser:
    def __init__(self, tokens: TokensFile, filename: str, folder: str):
        self.tokens = tokens
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

            if self.line_count == 23:
                if buffer == '" ':
                    pass

            if _looks_like_string(buffer):
                buffer += char
                i += 1

            # Check for newline
            elif char == '\n':
                self.line_count += 1  # Increment line count
                i += 1
                continue

            # Check for whitespace
            elif char.isspace():
                buffer = self.add_from_buffer(buffer, tokens)
                i += 1
                continue

            # Check for delimiters
            elif char in self.tokens.delimiters:
                buffer = self.add_from_buffer(buffer, tokens)
                tokens.append((self.tokens.delimiters_identifier[char], "DELIMITER", char))
                i += 1

            # Check for operators
            elif char in self.tokens.operators:
                buffer = self.add_from_buffer(buffer, tokens)
                # Check for multi-character operators
                composed_operator = char + code[i + 1] if i + 1 < len(code) else None
                if i + 1 < len(code) and composed_operator in self.tokens.operators:
                    tokens.append((self.tokens.operators_identifier[composed_operator], "OPERATOR", composed_operator))
                    i += 2
                else:
                    tokens.append((self.tokens.operators_identifier[char], "OPERATOR", char))
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
        if token in self.tokens.keywords:
            return self.tokens.keywords_identifier[token], "KEYWORD", token

        # Check for integer constants
        elif token.isdigit():
            return -1, "CONSTANT", int(token)

        # Check for floating-point constants
        elif token.replace('.', '', 1).isdigit() and token.count('.') == 1:
            return -1, "CONSTANT", float(token)

        # Check for string constants (single or double quotes)
        elif _is_string(token):
            return -1, "CONSTANT", token.strip('"').strip("'")  # Strip quotes from the string value

        # Check for valid identifier
        elif self.identifier_pattern.match(token):
            return -2, "IDENTIFIER", token

        # If none of the above, return an error for invalid identifier
        else:
            raise LexicalParsingError(file=self.filename, line=self.line_count, token=token)
