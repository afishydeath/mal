from types_ import (
    MalBoolean,
    MalList,
    MalNil,
    MalNumber,
    MalType,
)
from printer import pr_str


def add(a: MalNumber, b: MalNumber) -> MalNumber:
    return a + b


def sub(a: MalNumber, b: MalNumber) -> MalNumber:
    return a - b


def mul(a: MalNumber, b: MalNumber) -> MalNumber:
    return a * b


def div(a: MalNumber, b: MalNumber) -> MalNumber:
    return a // b


def prn(a: MalType) -> MalNil:
    print(pr_str(a, readably=True))
    return MalNil()


def list_(*a: MalType) -> MalList:
    return MalList(a)


def is_list(a: MalType) -> MalBoolean:
    return MalBoolean(isinstance(a, MalList))


def is_empty(a: MalList) -> MalBoolean:
    return MalBoolean(a == MalList([]))


def count(a: MalList) -> MalNumber:
    return MalNumber(len(a))


def eq(a: MalType, b: MalType) -> MalBoolean:
    return MalBoolean(a == b)
