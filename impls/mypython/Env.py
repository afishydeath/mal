from m_types import MalList, MalNil, MalNotFound, MalSymbol, MalType


class Env:
    def __init__(
        self,
        outer: "MalEnvOrNil",
        binds: MalList = MalList(),
        exprs: MalList = MalList(),
    ) -> None:
        self.outer: "MalEnvOrNil" = outer
        self.data: dict[MalType, MalType] = {}
        for i in range(len(binds)):
            if binds[i] != "&":
                self.data[binds[i]] = exprs[i]
            else:
                self.data[binds[i + 1]] = MalList(exprs[i:])
                break

    def set(self, key: MalSymbol, value: MalType) -> None:
        self.data[key] = value

    def get(self, key: MalSymbol) -> MalType:
        if key in self.data:
            return self.data[key]
        elif not isinstance(self.outer, MalNil):
            return self.outer.get(key)
        else:
            raise MalNotFound(f"'{key}' not found")


MalEnvOrNil = MalNil | Env
