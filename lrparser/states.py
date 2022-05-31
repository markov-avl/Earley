class State:
    __slots__ = [
        'NORMAL',
        'RETURN',
        'FINAL',
        '_symbol'
    ]
    
    def __init__(self, symbol: str):
        self._symbol = symbol

    def __eq__(self, other) -> bool:
        return self._symbol == other.symbol

    def __str__(self) -> str:
        return self._symbol

    def is_normal(self) -> bool:
        return self._symbol == 'q'

    def is_return(self) -> bool:
        return self._symbol == 'b'

    def is_final(self) -> bool:
        return self._symbol == 't'

    @property
    def symbol(self) -> str:
        return self._symbol


State.NORMAL = State('q')
State.RETURN = State('b')
State.FINAL = State('t')
