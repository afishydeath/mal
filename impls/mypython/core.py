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


def _pr_str(*args):
    out = " ".join([pr_str(arg, print_readably=True) for arg in args])
    return MalString(out)


def _str(*args):
    out = "".join([pr_str(arg, print_readably=False) for arg in args])
    # print(out)
    return MalString(out)


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
    "println": MalFunction(println),
    "pr-str": MalFunction(MalFunction(_pr_str)),
    "str": MalFunction(_str),
    "list": MalFunction(lambda *args: MalList(args)),
    "list?": MalFunction(lambda a: MalTrue() if isinstance(a, MalList) else MalFalse()),
    "empty?": MalFunction(lambda a: MalTrue() if a == MalList([]) else MalFalse()),
    "count": MalFunction(lambda a: MalNumber(len(a))),
}
