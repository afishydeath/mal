from typing import Callable, Dict, List
import enum
import re


class List_(List["Form"]):
    def __str__(self, readably=True) -> str:
        return "(" + (" ".join([x.__str__(readably=readably) for x in self])) + ")"


class Vector(List["Form"]):
    def __str__(self, readably=True) -> str:
        return "[" + (" ".join([x.__str__(readably=readably) for x in self])) + "]"


class Map(Dict["Form", "Form"]):
    def from_list(self, contents: List["Form"]) -> "Map":
        key: Form | None = None
        for form in contents:
            if key:
                self[key] = form
                key = None
            else:
                key = form
        if key:
            raise Exception(f"odd mappings, no val for {key}")
        return self

    def __str__(self, readably=True) -> str:
        to_join: List[str] = []
        for x in self:
            to_join.append(x.__str__(readably=readably))
            to_join.append(self[x].__str__(readably=readably))
        return "{" + " ".join(to_join) + "}"


subs = {"\\": "\\\\", "\n": "\\n", '"': '\\"'}


class String(str):
    def __str__(self, readably=True) -> str:
        text = super().__str__()
        if readably:
            return f'"{re.sub(r'[\\"\n]', lambda x: subs[x.group()], text)}"'
        else:
            return text


class Symbol(str):
    def __str__(self, readably=True) -> str:
        return self


class Keyword(str):
    def __str__(self, readably=True) -> str:
        return ":" + self


class Number(int):
    def __str__(self, readably=True) -> str:
        return super().__str__()


class Nil(enum.Enum):
    NIL = None

    def __str__(self, readably=True) -> str:
        return "nil"

    def __len__(self) -> int:
        return 0


class Boolean(enum.Enum):
    TRUE = True
    FALSE = False

    def __str__(self, readably=True) -> str:
        return "true" if self.value else "false"


class Fn:
    def __init__(self, impl: "Form", params: List_ | Vector, env, fn: Callable):
        self.impl = impl
        self.params = params
        self.env = env
        self.fn = fn

    def __call__(self):
        return self.fn()


Form = List_ | Vector | Map | String | Symbol | Keyword | Number | Nil | Boolean | Fn
