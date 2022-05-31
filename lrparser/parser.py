from .rule import Rule
from .configuration import Configuration
from .trace import Trace


class Parser:
    def __init__(self, rules: list[str], enter: str):
        self._rules = list(map(Rule, rules))
        self._enter = enter.replace(' ', '')
        self._s = self._rules[0].left
        self._configuration = None
        self._trace = None

    def run(self):
        self._configuration = Configuration.get_lrparser_configuration(self._s)
        self._trace = [Trace(step=0, configuration=self._configuration.copy())]
        self.tree_growth()
        return self._trace

    def tree_growth(self) -> None:
        """
        Шаг 1
        """
        while True:
            for rule in self._rules:
                if rule.left == self._configuration.store_2.top():
                    self._configuration.store_1.add(self._configuration.store_2.pop() + '0')
                    for symbol in rule.right[::-1]:
                        self._configuration.store_2.add(symbol)
                    self._trace.append(Trace(step=1, configuration=self._configuration.copy()))
                    break
            else:
                break
        self.successful_comparison()

    def successful_comparison(self) -> None:
        """
        Шаг 2
        """
        while self._configuration.index < len(self._enter) and \
                self._configuration.store_2.top() == self._enter[self._configuration.index]:
            self._configuration.store_1.add(self._configuration.store_2.pop())
            self._configuration.inc_index()
            self._trace.append(Trace(step=2, configuration=self._configuration.copy()))
        self.successful_completion()

    def successful_completion(self) -> None:
        """
        Шаг 3
        """
        # TODO: str(self._configuration.store_2) == '#' [хардкод]
        if self._configuration.index == len(self._enter) and str(self._configuration.store_2) == '#':
            self._configuration.set_final()
            self._configuration.store_2.pop()
            # TODO: [хардкод]
            self._configuration.store_2.add('$')
            self._trace.append(Trace(step=3, configuration=self._configuration.copy()))
        else:
            self.unsuccessful_comparison()

    def unsuccessful_comparison(self) -> None:
        """
        Шаг 4
        """
        if self._configuration.store_2.top() != self._s:
            self._configuration.set_return()
            self._trace.append(Trace(step=4, configuration=self._configuration.copy()))
        self.return_on_input()

    def return_on_input(self) -> None:
        """
        Шаг 5
        """
        if self._configuration.state.is_return():
            self._configuration.store_2.add(self._configuration.store_1.pop())
            self._configuration.dec_index()
            self._trace.append(Trace(step=5, configuration=self._configuration.copy()))
        self.alternative_replacement()

    def alternative_replacement(self) -> None:
        """
        Шаг 6.1
        """
        try:
            a, j = self._configuration.store_1.top()
            j = int(j)
            a_rules = [rule for rule in self._rules if rule.left == a]
            if j + 1 < len(a_rules):
                self._configuration.store_1.pop()
                for _ in a_rules[j].right:
                    self._configuration.store_2.pop()
                self._configuration.store_1.add(a_rules[j + 1].left + str(j + 1))
                for symbol in a_rules[j + 1].right[::-1]:
                    self._configuration.store_2.add(symbol)
                self._configuration.set_normal()
                self._trace.append(Trace(step=6.1, configuration=self._configuration.copy()))
        except ValueError:
            pass
        self.stop_parsing()

    def stop_parsing(self) -> None:
        """
        Шаг 6.2
        """
        if self._configuration.index == 0 and self._configuration.store_2.top() == self._s:
            raise Exception('Цепочка не принадлежит языку')
        self.cancel_result_tree_growth()

    def cancel_result_tree_growth(self) -> None:
        """
        Шаг 6.3
        """
        try:
            a, j = self._configuration.store_1.top()
            j = int(j)
            if self._configuration.state.is_return() and j >= 0:
                a_rules = [rule for rule in self._rules if rule.left == a]
                self._configuration.store_1.pop()
                for _ in a_rules[j].right:
                    self._configuration.store_2.pop()
                self._configuration.store_2.add(a)
                self._trace.append(Trace(step=6.3, configuration=self._configuration.copy()))
                self.alternative_replacement()
            else:
                self.tree_growth()
        except ValueError:
            self.tree_growth()

    def homomorphism(self) -> str:
        return self._configuration.store_1.get_extended_output(self._rules)
