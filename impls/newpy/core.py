from types_ import (
    MalAtom,
    MalFn,
    MalFnTCO,
    MalMap,
    MalString,
    MalSymbol,
    MalVector,
    malBool,
    MalBoolean,
    MalList,
    MalNil,
    MalNumber,
    MalType,
)
from reader import read_str
import logging

logger = logging.getLogger(__name__)


def add(a: MalNumber, b: MalNumber) -> MalNumber:
    return a + b


def sub(a: MalNumber, b: MalNumber) -> MalNumber:
    return a - b


def mul(a: MalNumber, b: MalNumber) -> MalNumber:
    return a * b


def div(a: MalNumber, b: MalNumber) -> MalNumber:
    return a // b


def prn(*a: MalType) -> MalNil:
    print(" ".join([x.__str__(readably=True) for x in a]))
    return MalNil()


def pr_str_(*a: MalType) -> MalString:
    logger.info(a)
    tmp = [x.__str__(readably=True) for x in a]
    logger.info(tmp)
    out = MalString(" ".join(tmp))
    logger.info(out)
    return out


def str_(*a: MalType) -> MalString:
    return MalString("".join([str(x) for x in a]))


def println(*a: MalType) -> MalNil:
    print(" ".join([str(x) for x in a]))
    return MalNil()


def read_string(a: MalString) -> MalType:
    return read_str(a.value)


def slurp(a: MalString) -> MalString:
    with open(a.value, "r") as f:
        return MalString(f.read())


def list_(*a: MalType) -> MalList:
    return MalList(list(a))


def is_list(a: MalType) -> MalBoolean:
    # logger.info(a)
    return malBool(isinstance(a, MalList))


def is_empty(a: MalList) -> MalBoolean:
    return malBool(a == MalList())


def count(a: MalList) -> MalNumber:
    return MalNumber(len(a))


def eq(a: MalType, b: MalType) -> MalBoolean:
    return malBool(a == b)


def lt(a: MalType, b: MalType) -> MalBoolean:
    return malBool(a < b)


def le(a: MalType, b: MalType) -> MalBoolean:
    return malBool(a <= b)


def gt(a: MalType, b: MalType) -> MalBoolean:
    return malBool(a > b)


def ge(a: MalType, b: MalType) -> MalBoolean:
    return malBool(a >= b)


def atom(a: MalType) -> MalAtom:
    return MalAtom(a)


def is_atom(a: MalType) -> MalBoolean:
    return malBool(isinstance(a, MalAtom))


def deref(a: MalAtom) -> MalType:
    return a.value


def reset(a: MalAtom, b: MalType) -> MalType:
    a.value = b
    return b


def swap(a: MalAtom, b: MalFn | MalFnTCO, *c: MalType) -> MalType:
    match b:
        case MalFn():
            a.value = b(a.value, *c)
        case MalFnTCO():
            a.value = b.fn(a.value, *c)
        case _:
            raise TypeError(f"Value {b} is not callable.")
    return a.value


def cons(a: MalType, b: MalList | MalVector) -> MalList:
    return MalList([a] + b.value)


def concat(*a: MalList | MalVector) -> MalList:
    out = MalList()
    for lis in a:
        for val in lis.value:
            out.append(val)
    return out


def vec(a: MalList | MalVector) -> MalVector:
    match a:
        case MalList():
            return MalVector(a.value)
        case _:
            return a


ns = {
    "+": add,
    "-": sub,
    "*": mul,
    "/": div,
    "prn": prn,
    "pr-str": pr_str_,
    "str": str_,
    "println": println,
    "read-string": read_string,
    "slurp": slurp,
    "list": list_,
    "list?": is_list,
    "empty?": is_empty,
    "count": count,
    "=": eq,
    "<": lt,
    "<=": le,
    ">": gt,
    ">=": ge,
    "atom": atom,
    "atom?": is_atom,
    "deref": deref,
    "reset!": reset,
    "swap!": swap,
    "cons": cons,
    "concat": concat,
    "vec": vec,
}
