from typing import Callable, Dict
from m_types import Form


class Env(Dict[Form, Form | Callable]):
    def __init__(self, outer: "Env|None", contents: Dict[Form, Form | Callable] = {}):
        self._outer: "Env|None" = outer
        if contents:
            super().__init__(contents)

    # def get_(self, key: Form) -> Form | Callable | None:
    #     if key in self:
    #         return self[key]
    #     if self._outer and (outer_check := self._outer.get_(key)) is not None:
    #         return outer_check
    #     return None

    def __contains__(self, key: object, /) -> bool:
        if super().__contains__(key):
            return True
        elif self._outer:
            return self._outer.__contains__(key)
        else:
            return False

    def __getitem__(self, key: Form, /) -> Form | Callable:
        if super().__contains__(key):
            return super().__getitem__(key)
        elif self._outer and key in self._outer:
            return self._outer[key]
        else:
            raise KeyError("key not in self or outer")
