import traceback

from Lab3.lexicalParser import LexicalParser, LexicalParsingError
from Lab2.hashTable import HashTable

import logging

from Lab3.tokensFile import TokensFile

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ProgramInternalForm:
    def __init__(self, lexical_parser: LexicalParser):
        self.pif = []
        self.constants_syt = HashTable()
        self.identifiers_syt = HashTable()
        self.lexicalParser = lexical_parser

    def parse(self):
        try:
            tokens = self.lexicalParser.parse_file()
            self.add_tokens_in_pif(tokens)

        except LexicalParsingError as e:
            logger.error(e)

        except Exception as e:
            traceback.print_exc()
            logger.error("Unknown Exception" + e.__str__())

    def add_tokens_in_pif(self, tokens):
        for token in tokens:
            if token[1] == "CONSTANT":
                pos = self.constants_syt.add(token[2])
                self.pif.append((token[0], token[1], pos))
            elif token[1] == "IDENTIFIER":
                pos = self.identifiers_syt.add(token[2])
                self.pif.append((token[0], token[1], pos))
            else:
                self.pif.append(token)

    def __str__(self):
        return "\n".join([f"{index}: {token}" for index, token in enumerate(self.pif)]) + "\n" + \
                f"\nConstants SYT: {self.constants_syt}\n" + \
                f"\nIdentifier SYT: {self.identifiers_syt}"


def run_pif():
    tokens_file = TokensFile()
    lexical_parser = LexicalParser(tokens_file, "p3.mylang", "Lab1")
    pif = ProgramInternalForm(lexical_parser)
    pif.parse()
    print(pif)


if __name__ == '__main__':
    run_pif()
