import traceback
from collections import defaultdict
from email.policy import default

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

        self.syt_mapper = {
            "CONSTANT": self.constants_syt,
            "IDENTIFIER": self.identifiers_syt
        }

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

    def compare_values(self, symbol, index):
        pif_value = self.pif[index]
        return str(symbol) == str(pif_value[2])

    def get_constant_value(self, index):
        pif_value = self.pif[index]
        syt: HashTable = self.syt_mapper[pif_value[1]]
        syt_location, pos = pif_value[2]
        return str(syt.search(syt_location, pos))

    def is_constant_or_identifier(self, pif_index):
        return self.pif[pif_index][1] in ["CONSTANT", "IDENTIFIER"]

    def capitalized_type(self, pif_index):
        return self.pif[pif_index][1].lower().capitalize()

    def print_up_to(self, index):
        return "\n".join([f"{index}: {token}" for index, token in enumerate(self.pif[:index + 1])]) + "\n" + \
                f"\nConstants SYT: {self.constants_syt}\n" + \
                f"\nIdentifier SYT: {self.identifiers_syt}"

    def __str__(self):
        return "\n".join([f"{index}: {token}" for index, token in enumerate(self.pif)]) + "\n" + \
                f"\nConstants SYT: {self.constants_syt}\n" + \
                f"\nIdentifier SYT: {self.identifiers_syt}"

    def __len__(self):
        return len(self.pif)

def run_pif():
    tokens_file = TokensFile()
    lexical_parser = LexicalParser(tokens_file, "p3.mylang", "Lab1")
    pif = ProgramInternalForm(lexical_parser)
    pif.parse()
    print(pif)


if __name__ == '__main__':
    run_pif()
