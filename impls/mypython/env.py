from typing import Callable, Dict, List, Tuple
from m_types import Form, List_, Symbol


class Env(Dict[Form, Form | Callable]):
    def __init__(
        self,
        outer: "Env|None",
        binds: List[Form] = [],
        exprs: List[Form | Callable] | Tuple[Form | Callable] = [],
    ):
        self._outer: "Env|None" = outer
        for p in range(len(binds)):
            if binds[p] == Symbol("&"):
                self[binds[p + 1]] = List_(exprs[p:])  # type: ignore --remove in step 5
                break
            self[binds[p]] = exprs[p]

    def __contains__(self, key: object, /) -> bool:
        if super().__contains__(key):
            return True
        elif self._outer is not None:
            return key in self._outer
        else:
            return False

    def __getitem__(self, key: Form, /) -> Form | Callable:
        if super().__contains__(key):
            return super().__getitem__(key)
        elif self._outer is not None and key in self._outer:
            return self._outer[key]
        else:
            raise KeyError("key not in self or outer")

    def __str__(self) -> str:
        return super().__str__() + f" -> {str(self._outer)}"
