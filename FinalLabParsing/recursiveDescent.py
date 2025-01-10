from Lab3.lexicalParser import LexicalParser
from Lab3.pif import ProgramInternalForm
from FinalLabParsing.grammar import load_grammar
from Lab3.tokensFile import TokensFile
from Lab6.recursiveDescent import SimpleRecursiveDescentParser


class ComplexRecursiveDescentParser(SimpleRecursiveDescentParser):
    def __init__(self, grammar: dict, pif: ProgramInternalForm, output_activated=True):
        super().__init__(
            grammar=grammar,
            input_string="",
            output_activated=output_activated
        )
        self.pif = pif

    @property
    def print_input_string(self):
        return str(self.pif.pif[self.position])

    @property
    def finished_reading(self):
        return self.position == self.pif.__len__()

    @property
    def advance_condition(self):
        return self.position < self.pif.__len__()

    def print_progress(self):
        self._print(self.pif.print_up_to(self.position))

    def _compare_values(self, symbol):
        if self.pif.is_constant_or_identifier(self.position):
            # In this case, we create a simple RcuDp object to parse the constant/identifier
            # with the entry point being the parent
            parser = SimpleRecursiveDescentParser(
                grammar=self.grammar,
                input_string=self.pif.get_constant_value(self.position),
                output_activated=True
            )
            return parser.parse(starting_non_terminal=self.pif.capitalized_type(self.position))

        return self.pif.compare_values(symbol, self.position)


def main():
    grammar = load_grammar("../Lab1b/parsing_rules.in")
    tokens_file = TokensFile()
    lexical_parser = LexicalParser(tokens_file, "p3.mylang", "Lab1")
    pif = ProgramInternalForm(lexical_parser)
    pif.parse()

    parser = ComplexRecursiveDescentParser(
        grammar=grammar,
        pif=pif,
        output_activated=True
    )

    match = parser.parse(starting_non_terminal="Program")
    if match:
        print("The program is accepted.")

    print(pif)


if __name__ == "__main__":
    main()
