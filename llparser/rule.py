class Rule:
    def __init__(self, rule: str):
        self._rule = rule.replace(' ', '').split('->')

    @property
    def left(self) -> str:
        return self._rule[0]

    @property
    def right(self) -> str:
        return self._rule[1]

    @property
    def alpha(self) -> str:
        return self._rule[1][:-1]

    @property
    def beta(self) -> str:
        return self._rule[1][-1]
