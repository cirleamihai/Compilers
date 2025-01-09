from grammar import load_grammar

class RecursiveDescentParser:
    def __init__(self, grammar: dict, input_string: str):
        self.grammar = grammar
        self.input_string = input_string
        self.position = 0
        self.success = False
        self.history = []  # Stack to keep track of backtracking

    def parse(self, starting_non_terminal):
        self.success = False
        self.position = 0
        self.history = []

        # Start expanding the starting non-terminal
        self._expand(starting_non_terminal)

        if self.success and self.position == self.input_string.__len__():
            return True

        else:
            return False

    def _expand(self, non_terminal):
        rules = self.grammar[non_terminal]  # Get the production rule for the non-terminal

        for rule in rules:
            print("Expanding", non_terminal, "with", rule)
            self.history.append(("expand", non_terminal, self.position, rule))

            # Checking the rule
            self._try_rule(rule)
            if self.success:
                return

    def _advance(self, symbol):
        if self.position < self.input_string.__len__() and self.input_string[self.position] == symbol:
            self.position += 1
            print(f"Advanced to {self.position} with {symbol}")
            return True

        return False

    def _momentary_insuccess(self):
        print("Momentary Insuccess...")
        return self._back()

    def _back(self):
        action, non_terminal, position, rule = self.history.pop()
        self.position = position

        print(f"Non terminal {non_terminal} failed to {action} with rule {rule}. Position: {position}")
        return False

    def _try_rule(self, rule):
        for symbol in rule:
            if symbol.isupper():
                self._expand(symbol)
                if not self.success:
                    return self._momentary_insuccess()

            else:
                if not self._advance(symbol):
                    return self._momentary_insuccess()

        self._success()

    def _success(self):
        print("This rule is successful!")
        self.success = True

def check_starting_terminals(grammar: dict, input_str: str) -> list:
    starting_non_terminals = []

    for non_terminal, rules in grammar.items():
        for rule in rules:
            if rule[0] == input_str[0]:
                starting_non_terminals.append(non_terminal)
                break

    return starting_non_terminals

def main():
    grammar = load_grammar('rules.in')
    input_string = "aabcbaa"
    matches = False

    starting_non_terminals = check_starting_terminals(grammar, input_string)

    for starting_non_terminal in starting_non_terminals:
        print("\n\nTrying to parse with starting non-terminal", starting_non_terminal)
        parser = RecursiveDescentParser(grammar, input_string)
        if parser.parse(starting_non_terminal):
            print("Input string is accepted!")
            matches = True
            break

    if not matches:
        print("Input string is not accepted!")

if __name__ == "__main__":
    main()
