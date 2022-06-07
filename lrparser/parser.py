from .grammar import Grammar
from .configuration import Configuration
from .trace import Trace


class Parser:
    def __init__(self, grammar: Grammar):
        self._grammar = grammar
        self._configuration = None
        self._enter = None
        self._trace = None

    @property
    def grammar(self) -> Grammar:
        return self._grammar

    @grammar.setter
    def grammar(self, grammar: Grammar) -> None:
        self._grammar = grammar

    def run(self, enter: str):
        self._configuration = Configuration.get_lrparser_configuration(self._grammar.s)
        self._enter = enter.replace(' ', '')
        self._trace = [Trace(0, self._configuration.copy())]
        self._tree_growth()
        return self._trace

    def _tree_growth(self) -> None:
        """
        Шаг 1
        """
        while True:
            for rule in self._grammar.rules:
                if rule.left == self._configuration.store_2.top():
                    self._configuration.store_1.add(self._configuration.store_2.pop() + '0')
                    for symbol in rule.right[::-1]:
                        self._configuration.store_2.add(symbol)
                    self._make_trace(1)
                    break
            else:
                break
        self._successful_comparison()

    def _successful_comparison(self) -> None:
        """
        Шаг 2
        """
        while self._configuration.index < len(self._enter) and \
                self._configuration.store_2.top() == self._enter[self._configuration.index]:
            self._configuration.store_1.add(self._configuration.store_2.pop())
            self._configuration.inc_index()
            self._make_trace(2)
        self._successful_completion()

    def _successful_completion(self) -> None:
        """
        Шаг 3
        """
        # TODO: str(self._configuration.store_2) == '#' [хардкод]
        if self._configuration.index == len(self._enter) and str(self._configuration.store_2) == '#':
            self._configuration.set_final()
            self._configuration.store_2.pop()
            # TODO: [хардкод]
            self._configuration.store_2.add('$')
            self._make_trace(3)
        else:
            self._unsuccessful_comparison()

    def _unsuccessful_comparison(self) -> None:
        """
        Шаг 4
        """
        if self._configuration.store_2.top() != self._grammar.s:
            self._configuration.set_return()
            self._make_trace(4)
        self._return_on_input()

    def _return_on_input(self) -> None:
        """
        Шаг 5
        """
        if self._configuration.state.is_return():
            self._configuration.store_2.add(self._configuration.store_1.pop())
            self._configuration.dec_index()
            self._make_trace(5)
        self._alternative_replacement()

    def _alternative_replacement(self) -> None:
        """
        Шаг 6.1
        """
        try:
            a, j = self._configuration.store_1.top()
            j = int(j)
            a_rules = [rule for rule in self._grammar.rules if rule.left == a]
            if j + 1 < len(a_rules):
                self._configuration.store_1.pop()
                for _ in a_rules[j].right:
                    self._configuration.store_2.pop()
                self._configuration.store_1.add(a_rules[j + 1].left + str(j + 1))
                for symbol in a_rules[j + 1].right[::-1]:
                    self._configuration.store_2.add(symbol)
                self._configuration.set_normal()
                self._make_trace(6.1)
        except ValueError:
            pass
        self._stop_parsing()

    def _stop_parsing(self) -> None:
        """
        Шаг 6.2
        """
        if self._configuration.index == 0 and self._configuration.store_2.top() == self._grammar.s:
            raise Exception('Цепочка не принадлежит языку')
        self._cancel_result_tree_growth()

    def _cancel_result_tree_growth(self) -> None:
        """
        Шаг 6.3
        """
        try:
            a, j = self._configuration.store_1.top()
            j = int(j)
            if self._configuration.state.is_return() and j >= 0:
                a_rules = [rule for rule in self._grammar.rules if rule.left == a]
                self._configuration.store_1.pop()
                for _ in a_rules[j].right:
                    self._configuration.store_2.pop()
                self._configuration.store_2.add(a)
                self._make_trace(6.3)
                self._alternative_replacement()
            else:
                self._tree_growth()
        except ValueError:
            self._tree_growth()

    def _make_trace(self, step: float | int) -> None:
        self._trace.append(Trace(step, self._configuration.copy()))

    def homomorphism(self) -> str:
        return self._configuration.store_1.get_extended_output(self._grammar.rules)
