from types_ import MalMap, MalNil, MalSymbol, MalType
import logging

logger = logging.getLogger(__name__)


class Env:
    def __init__(self, outer: "Env|MalNil"):
        self.outer = outer
        self.data = MalMap()

    def set(self, key: MalSymbol, value: MalType) -> None:
        self.data[key] = value

    def get(self, key: MalSymbol) -> MalType:
        if key in self.data:
            return self.data[key]
        elif not isinstance(self.outer, MalNil):
            return self.outer.get(key)
        else:
            raise KeyError(f"Key {key} not in env")

    def __contains__(self, key):
        return (key in self.data) or ((key in self.outer) if self.outer else False)

    def __str__(self) -> str:
        return str(self.outer) if self.outer else "" + str(self.data)
