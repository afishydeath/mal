from typing import Dict, List
import enum
import re


class List_(List["Form"]):
    pass


class Vector(List["Form"]):
    pass


class Map(Dict["Form", "Form"]):
    def from_list(self, contents: List["Form"]) -> "Map":
        key: Form | None = None
        for form in contents:
            if key:
                self[key] = form
                key = None
            elif isinstance(form, (Keyword, Symbol)):
                key = form
            else:
                raise Exception("invalid key")
        if key:
            raise Exception(f"odd mappings, no val for {key}")
        return self


class String(str):
    pass


class Symbol(str):
    pass


class Keyword(str):
    pass


class Number(int):
    pass


class Nil(enum.Enum):
    NIL = None


class Boolean(enum.Enum):
    TRUE = True
    FALSE = False


Form = List_ | Vector | Map | String | Symbol | Keyword | Number | Nil | Boolean
