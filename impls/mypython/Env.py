from m_types import MalNil, MalNotFound, MalSymbol, MalType


class Env:
    def __init__(self, outer: "MalEnvOrNil") -> None:
        self.outer: "MalEnvOrNil" = outer
        self.data : dict[MalSymbol, MalType] = {}

    def set(self, key: MalSymbol, value: MalType) -> None:
        self.data[key] = value

    def get(self, key: MalSymbol) -> MalType:
        if key in self.data:
            return self.data[key]
        elif not isinstance(self.outer,MalNil):
            return self.outer.get(key)
        else:
            raise MalNotFound(f"'{key}' not found")
        
MalEnvOrNil = (MalNil | Env)
