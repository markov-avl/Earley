class Grammar:
    def __init__(self, start=None, productions=None):
        self.productions = dict() if productions is None else productions
        self.start = start

    def add(self, left, right):
        if left not in self.productions:
            self.productions[left] = list()
        self.productions[left].append(right)
        return self

    def set_start(self, nonterminal):
        self.start = nonterminal

    def is_terminal(self, symbol):
        return not self.is_nonterminal(symbol)

    def is_nonterminal(self, symbol):
        return symbol in self.productions
