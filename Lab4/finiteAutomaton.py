import json


class DFA:
    def __init__(self, states, alphabet, transition_function, start_state, accept_states):
        self.states = states  # Set of states
        self.alphabet = alphabet  # Input symbols
        self.transition_function = transition_function  # Transition rules
        self.current_state = start_state  # Current state starts at the start state
        self.start_state = start_state  # Start state
        self.accept_states = accept_states  # Set of accept states

    def reset(self):
        """Reset to the start state."""
        self.current_state = self.start_state

    def process(self, input_string):
        """Process an input string and check if it's accepted."""
        self.reset()  # Ensure we start from the beginning
        for symbol in input_string:
            if symbol not in self.alphabet:
                raise ValueError(f"Invalid symbol '{symbol}' for this DFA.")
            self.current_state = self.transition_function.get(
                (self.current_state, symbol), None
            )
            if self.current_state is None:
                return False  # If no valid transition exists, reject

        return self.current_state in self.accept_states  # Check if in accept state


with open("FA.in") as file:
    lines = file.read()
    json_content = json.loads(lines)

    states = json_content["states"]
    alphabet = json_content["alphabet"]
    transition_function = {}
    for from_keys, vals in json_content["transition_function"].items():
        for with_alphabet, to_result in vals.items():
            transition_function[from_keys, with_alphabet] = to_result

    start_state = json_content["start_state"]
    accept_states = json_content["accept_states"]


# Create DFA instance
dfa = DFA(states, alphabet, transition_function, start_state, accept_states)

# Test the DFA
test_strings = ["bbab", "ba", "ab", "a", "b", "abab", "aaaaab", "aba"]
for string in test_strings:
    result = dfa.process(string)
    print(f"String '{string}' is {'ACCEPTED' if result else 'REJECTED'}")