from .rule import Rule
from .states import State
from .configuration import Configuration
from .trace import Trace


class Parser:
    def __init__(self, rules: list[str], enter: str):
        self._rules = list(map(Rule, rules))
        self._enter = enter.replace(' ', '')
        self._s = self._rules[0].left
        self._configuration = None
        self._trace = None

    def run(self) -> list[Trace]:
        self._configuration = Configuration()
        self._trace = [Trace(step=0, configuration=self._configuration.copy())]
        self.convolution_attempt()
        return self._trace

    def convolution_attempt(self):
        """
        Шаг 1
        """
        while True:
            for j, rule in list(enumerate(self._rules)):
                if self._configuration.store_1.endswith(rule.right):
                    for i in range(len(rule.right)):
                        self._configuration.pop_store_1()
                    self._configuration.add_to_store_1(rule.left)
                    self._configuration.add_to_store_2(j)
                    self._trace.append(Trace(step=1, configuration=self._configuration.copy()))
                    break
            else:
                break
        self.transfer()

    def transfer(self):
        """
        Шаг 2
        """
        if self._configuration.index != len(self._enter):
            self._configuration.add_to_store_1(self._enter[self._configuration.index])
            self._configuration.add_to_store_2('s')
            self._configuration.inc_index()
            self._trace.append(Trace(step=2, configuration=self._configuration.copy()))
            self.convolution_attempt()
        else:
            self.assumption()

    def assumption(self):
        """
        Шаг 3
        """
        if self._configuration.state == State.NORMAL and \
                self._configuration.index == len(self._enter) and \
                self._configuration.store_1 == '#' + self._s:
            self._configuration.set_final()
            self._trace.append(Trace(step=3, configuration=self._configuration.copy()))
        else:
            self.transition_to_return_state()

    def transition_to_return_state(self):
        """
        Шаг 4
        """
        if self._configuration.state == State.NORMAL and \
                self._configuration.index == len(self._enter) and \
                self._configuration.store_1 != self._s:
            self._configuration.set_return()
            self._trace.append(Trace(step=4, configuration=self._configuration.copy()))
        self.return_to_the_previous_convolution()

    def return_to_the_previous_convolution(self) -> None:
        """
        Шаг 5.1
        """
        j = self._configuration.top_store_2()
        if self._configuration.state == State.RETURN and isinstance(j, int) and \
                self._configuration.top_store_1() == self._rules[j].left:
            for k, rule in list(enumerate(self._rules))[j + 1:]:
                if rule.right == self._rules[j].right:
                    self._configuration.set_normal()
                    self._configuration.pop_store_1()
                    self._configuration.add_to_store_1(rule.left)
                    self._configuration.pop_store_2()
                    self._configuration.add_to_store_2(k)
                    self._trace.append(Trace(step=5.1, configuration=self._configuration.copy()))
                    self.convolution_attempt()
                    return
        self.undoing_an_earlier_convolution()

    def undoing_an_earlier_convolution(self) -> None:
        """
        Шаг 5.2
        """
        if self._configuration.state == State.RETURN and self._configuration.index == len(self._enter):
            j = self._configuration.top_store_2()
            if isinstance(j, int) and self._configuration.top_store_1() == self._rules[j].left:
                self._configuration.pop_store_1()
                self._configuration.add_to_store_1(self._rules[j].right)
                self._configuration.pop_store_2()
                self._trace.append(Trace(step=5.2, configuration=self._configuration.copy()))
                self.return_to_the_previous_convolution()
                return
        self.performing_a_transferring()

    def performing_a_transferring(self) -> None:
        """
        Шаг 5.3
        """
        j = self._configuration.top_store_2()
        if self._configuration.state == State.RETURN and \
                self._configuration.index != len(self._enter) and \
                isinstance(j, int):
            for rule in self._rules[j + 1:]:
                if rule.right == self._rules[j].right:
                    break
            else:
                self._configuration.pop_store_1()
                self._configuration.add_to_store_1(self._rules[j].right)
                self._configuration.add_to_store_1(self._enter[self._configuration.index])
                self._configuration.pop_store_2()
                self._configuration.add_to_store_2('s')
                self._configuration.set_normal()
                self._configuration.inc_index()
                self._trace.append(Trace(step=5.3, configuration=self._configuration.copy()))
                self.convolution_attempt()
                return
        self.cancel_the_result_of_a_transfer_operation()

    def cancel_the_result_of_a_transfer_operation(self) -> None:
        """
        Шаг 5.4
        """
        if self._configuration.top_store_2() == 's':
            try:
                self._configuration.pop_store_1()
                self._configuration.pop_store_2()
                self._configuration.dec_index()
                self._trace.append(Trace(step=5.4, configuration=self._configuration.copy()))
            except Exception:
                raise Exception('Ошибка')
        self.return_to_the_previous_convolution()
