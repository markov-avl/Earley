import copy

from .states import State


class Configuration:
    def __init__(self):
        self._state = State.NORMAL
        self._index = 0
        self._store_1 = '#'
        self._store_2 = '$'

    @property
    def state(self) -> State:
        return self._state
        
    @property
    def index(self) -> int:
        return self._index

    @property
    def store_1(self) -> str:
        return self._store_1

    @property
    def store_2(self) -> str:
        return self._store_2

    def inc_index(self):
        self._index += 1

    def dec_index(self):
        self._index -= 1

    def add_to_store_1(self, symbol: str or int) -> None:
        self._store_1 += symbol if isinstance(symbol, str) else str(symbol + 1)

    def top_store_1(self) -> str or int:
        return int(self._store_1[-1]) - 1 if self._store_1[-1].isdigit() else self._store_1[-1]

    def pop_store_1(self) -> str or int:
        symbol = self.top_store_1()
        self._store_1 = self._store_1[: -1]
        return symbol

    def add_to_store_2(self, symbol: str or int) -> None:
        self._store_2 = (symbol if isinstance(symbol, str) else str(symbol + 1)) + self._store_2

    def top_store_2(self) -> str or int:
        return int(self._store_2[0]) - 1 if self._store_2[0].isdigit() else self._store_2[0]

    def pop_store_2(self) -> str:
        symbol = self.top_store_2()
        self._store_2 = self._store_2[1:]
        return symbol

    def set_normal(self) -> None:
        self._state = State.NORMAL

    def set_return(self) -> None:
        self._state = State.RETURN

    def set_final(self) -> None:
        self._state = State.FINAL

    def copy(self):
        return copy.copy(self)

    def __str__(self) -> str:
        return f'({self._state}, {self._index + 1}, {self._store_1}, {self._store_2})'
