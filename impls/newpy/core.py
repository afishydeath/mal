from types_ import (
    MalString,
    malBool,
    MalBoolean,
    MalList,
    MalNil,
    MalNumber,
    MalType,
)
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


ns = {
    "+": add,
    "-": sub,
    "*": mul,
    "/": div,
    "prn": prn,
    "pr-str": pr_str_,
    "str": str_,
    "println": println,
    "list": list_,
    "list?": is_list,
    "empty?": is_empty,
    "count": count,
    "=": eq,
    "<": lt,
    "<=": le,
    ">": gt,
    ">=": ge,
}
