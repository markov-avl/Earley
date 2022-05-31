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

    @property
    def symbol(self) -> str:
        return self._symbol


State.NORMAL = State('q')
State.RETURN = State('b')
State.FINAL = State('t')
