from m_types import (
    MalFalse,
    MalFunction,
    MalList,
    MalNil,
    MalNumber,
    MalString,
    MalTrue,
)
from printer import pr_str


def prn(*args):
    print(" ".join([pr_str(arg, print_readably=True) for arg in args]))
    return MalNil()


def println(*args):
    print(" ".join([pr_str(arg, print_readably=False) for arg in args]))
    return MalNil()


ns = {
    "+": MalFunction(lambda a, b: MalNumber(a + b)),
    "-": MalFunction(lambda a, b: MalNumber(a - b)),
    "*": MalFunction(lambda a, b: MalNumber(a * b)),
    "/": MalFunction(lambda a, b: MalNumber(a / b)),
    "=": MalFunction(lambda a, b: MalTrue() if a == b else MalFalse()),
    "<": MalFunction(lambda a, b: MalTrue() if a < b else MalFalse()),
    "<=": MalFunction(lambda a, b: MalTrue() if a <= b else MalFalse()),
    ">": MalFunction(lambda a, b: MalTrue() if a > b else MalFalse()),
    ">=": MalFunction(lambda a, b: MalTrue() if a >= b else MalFalse()),
    "prn": MalFunction(prn),
    "pr-str": MalFunction(
        lambda *args: MalString(
            " ".join([pr_str(arg, print_readably=True) for arg in args])
        )
    ),
    "str": MalFunction(
        lambda *args: MalString(
            "".join([pr_str(arg, print_readably=False) for arg in args])
        )
    ),
    "list": MalFunction(lambda *args: MalList(args)),
    "list?": MalFunction(lambda a: MalTrue() if isinstance(a, MalList) else MalFalse()),
    "empty?": MalFunction(lambda a: MalTrue() if a == MalList([]) else MalFalse()),
    "count": MalFunction(lambda a: MalNumber(len(a))),
}
