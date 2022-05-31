from collections import deque

from .rule import Rule


class Store:
    DIGITS = '₁₂₃₄₅₆₇₈₉'

    def __init__(self, is_left: bool = True):
        self._store = deque()
        self._append = self._store.appendleft if is_left else self._store.append
        self._pop = self._store.popleft if is_left else self._store.pop
        self._first_element = 0 if is_left else -1

    def add(self, symbol: str or int) -> None:
        self._append(symbol)

    def pop(self) -> str or int:
        return self._pop()

    def top(self) -> str or int:
        return self._store[self._first_element]

    def get_output(self) -> str:
        return ''.join(symbol for symbol in self._store if symbol.islower())

    def get_extended_output(self, rules: list[Rule]) -> str:
        output = ''
        for symbol in self._store:
            if len(symbol) > 1:
                a, j = symbol
                output += str(rules.index([rule for rule in rules if rule.left == a][int(j)]) + 1)
        return output

    def __iter__(self):
        for item in self._store:
            yield item

    def __str__(self) -> str:
        new_store = deque()
        for symbol in self._store:
            new_store.append(f'{symbol[: -1]}{self.DIGITS[int(symbol[-1])]}' if symbol[-1].isdigit() else symbol)
        return ''.join(new_store)
