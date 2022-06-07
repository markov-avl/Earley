from lrparser.rule import Rule


class Grammar:
    def __init__(self, s: str, *rules):
        self._s = s
        self._rules = list(map(Rule, rules))

    @property
    def s(self) -> str:
        return self._s

    @property
    def rules(self) -> list[Rule]:
        return self._rules
