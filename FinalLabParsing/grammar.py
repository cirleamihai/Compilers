def load_grammar(filename):
    """
    Reads grammar rules from a file (e.g., rules.in) of the form:
        E -> T E'
        E' -> + T E' | e
        ...
    Returns a dictionary like:
        {
            'E':  [['T', "E'"]],
            "E'": [['+', 'T', "E'"], ['e']],
            ...
        }
    """
    grammar = {}

    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()

            if not line or '->' not in line:
                continue

            non_terminal, terminals = line.split('->')
            non_terminal = non_terminal.strip()

            raw_productions = terminals.split('|')
            productions = []

            for production in raw_productions:
                production = production.strip()
                symbol = production.split()
                if production == "":
                    symbol = [" "]
                productions.append(symbol)

            grammar[non_terminal] = productions

        return grammar