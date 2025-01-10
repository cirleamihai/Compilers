from grammar import load_grammar


class SimpleRecursiveDescentParser:
    def __init__(self, grammar: dict, input_string: str = "", output_activated=True):
        self.grammar = grammar
        self.input_string = input_string
        self.position = 0
        self.success = False
        self.history = []  # Stack to keep track of backtracking
        self.parsing_tree = []  # Tree node to keep track of the parse tree
        self.node_index = 1
        self.output_activated = output_activated

    def _print(self, *args, **kwargs):
        if self.output_activated:
            print(*args, **kwargs)

    @property
    def finished_reading(self):
        return self.position == self.input_string.__len__()

    def parse(self, starting_non_terminal):
        self.success = False
        self.position = 0
        self.history = []

        # Start expanding the starting non-terminal
        self._expand(starting_non_terminal)

        if self.success and self.finished_reading:
            return True

        else:
            return False

    def _expand(self, non_terminal, parent=None, parent_index=-1):
        rules = self.grammar[non_terminal]  # Get the production rule for the non-terminal

        for rule in rules:
            self._print("Expanding", non_terminal, "with", rule)
            self.history.append(("expand", non_terminal, self.position, rule))
            node_index = self._add_tree_node(non_terminal, parent=parent, parent_index=parent_index)

            # Checking the rule
            self._try_rule(rule, non_terminal, non_terminal_index=node_index)
            if self.success:
                return

            # If the rule is not successful, remove the tree node
            self._remove_tree_nodes(node_index)

    @property
    def advance_condition(self):
        return self.position < self.input_string.__len__()

    def _advance(self, symbol, parent, parent_index):
        if self.advance_condition and self._compare_values(symbol, parent=parent):
            self.position += 1
            self._add_tree_node(symbol=symbol, parent=parent, parent_index=parent_index)
            self._print(f"Advanced to {self.position} with {symbol}")
            return True

        return False

    def _compare_values(self, symbol, *args, **kwargs):
        return self.input_string[self.position] == symbol

    def _momentary_insuccess(self):
        self._print("Momentary Insuccess...")
        self.success = False
        return self._back()

    def _back(self):
        action, non_terminal, position, rule = self.history.pop()
        self.position = position

        self._print(f"Non terminal {non_terminal} failed to {action} with rule {rule}. Position: {position}")
        return False

    def _try_rule(self, rule, non_terminal, non_terminal_index=-1):
        # Handle epsilon (empty) rules
        if rule == ["e"]:
            self._print(f"Epsilon detected in rule for {non_terminal}.")
            self._success()  # Epsilon means immediate success
            return True

        for symbol in rule:
            if symbol.isupper():
                self._expand(symbol, parent=non_terminal, parent_index=non_terminal_index)
                if not self.success:
                    return self._momentary_insuccess()

            else:
                if not self._advance(symbol, parent=non_terminal, parent_index=non_terminal_index):
                    return self._momentary_insuccess()

        self._success()

    def _success(self):
        self._print("Patterns match so far!")
        self.success = True

    def _add_tree_node(self, symbol, parent, parent_index=-1):
        self.parsing_tree.append({
            "Node": symbol,
            "Parent": parent,
            "Parent Index": parent_index,
            "Index": self.node_index,
            "Sibling To Index": self._get_sibling(parent, parent_index),
        })

        self.node_index += 1
        return self.node_index - 1

    def _get_sibling(self, parent, parent_index):
        siblings = [node for node in self.parsing_tree if
                    node["Parent"] == parent and node["Parent Index"] == parent_index]
        return siblings[-1]["Index"] if siblings else -1

    def _remove_tree_nodes(self, first_bad_node_index):
        self.parsing_tree = [node for node in self.parsing_tree if node["Index"] < first_bad_node_index]
        self.node_index = first_bad_node_index

    def display_parsing_tree(self):
        import pandas as pd
        df = pd.DataFrame(self.parsing_tree)
        df = df.drop(columns=["Parent Index"])
        self._print("\nTree Format:")
        self._print(df.to_string(index=False))


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
    input_string = "aa"
    matches = False

    starting_non_terminals = check_starting_terminals(grammar, input_string)

    for starting_non_terminal in starting_non_terminals:
        print("\n\nTrying to parse with starting non-terminal", starting_non_terminal)
        parser = SimpleRecursiveDescentParser(grammar, input_string)
        if parser.parse(starting_non_terminal):
            print("Input string is accepted!")
            parser.display_parsing_tree()
            matches = True
            break

    if not matches:
        print("Input string is not accepted!")


if __name__ == "__main__":
    main()
