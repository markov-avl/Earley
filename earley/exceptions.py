class MultipleStartsError(Exception):
    def __init__(self):
        self.strerror = 'Multiple starting variables'
        super().__init__(self.strerror)


class EmptyGrammarError(Exception):
    def __init__(self):
        self.strerror = 'Empty grammar'
        super().__init__(self.strerror)


class InvalidNonterminalError(Exception):
    def __init__(self):
        self.strerror = 'Invalid nonterminal variable'
        super().__init__(self.strerror)


class GrammarException(Exception):
    def __init__(self, strerror=''):
        self.strerror = strerror
        super().__init__(self.strerror)
