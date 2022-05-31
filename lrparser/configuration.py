from .states import State
from .store import Store


class Configuration:
    def __init__(self):
        self._state = State.NORMAL
        self._index = 0
        self._store_1 = Store(False)
        self._store_2 = Store(True)

    @staticmethod
    def get_llparser_configuration():
        configuration = Configuration()
        configuration.store_1.add('#')
        configuration.store_1.add('$')
        return configuration

    @staticmethod
    def get_lrparser_configuration(start: str):
        configuration = Configuration()
        configuration.store_1.add('$')
        configuration.store_2.add('#')
        configuration.store_2.add(start)
        return configuration

    @property
    def state(self) -> State:
        return self._state
        
    @property
    def index(self) -> int:
        return self._index

    @property
    def store_1(self) -> Store:
        return self._store_1

    @property
    def store_2(self) -> Store:
        return self._store_2

    def inc_index(self):
        self._index += 1

    def dec_index(self):
        self._index -= 1

    def set_normal(self) -> None:
        self._state = State.NORMAL

    def set_return(self) -> None:
        self._state = State.RETURN

    def set_final(self) -> None:
        self._state = State.FINAL

    def copy(self):
        configuration = Configuration()
        # copy state
        if self._state.is_normal():
            configuration.set_normal()
        elif self._state.is_return():
            configuration.set_return()
        else:
            configuration.set_final()
        # copy index
        while configuration.index < self._index:
            configuration.inc_index()
        # copy store 1
        for item in self._store_1:
            configuration.store_1.add(item)
        # copy store 2
        for item in list(self._store_2)[::-1]:
            configuration.store_2.add(item)
        return configuration

    def __str__(self) -> str:
        return f'({self._state}, {self._index + 1}, {self._store_1}, {self._store_2})'
