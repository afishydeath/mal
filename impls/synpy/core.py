from types_ import (
    MalAtom,
    MalError,
    MalFalse,
    MalFn,
    MalFnTCO,
    MalKeyword,
    MalMap,
    MalSequence,
    MalString,
    MalSymbol,
    MalTrue,
    MalVector,
    malBool,
    MalBoolean,
    MalList,
    MalNil,
    MalNumber,
    MalType,
    Fn,
    hasMeta,
    to_mal_type,
)
from reader import read_str
import logging
import time

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
    logger.info(a)
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


def deref(a: MalAtom) -> MalType:
    return a.value


def reset(a: MalAtom, b: MalType) -> MalType:
    a.value = b
    return b


def swap(a: MalAtom, b: MalFn | MalFnTCO, *c: MalType) -> MalType:
    a.value = b(a.value, *c)
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


def nth(a: MalList | MalVector, b: MalNumber) -> MalType:
    return a[b.value]


def first(a: MalList | MalVector | MalNil) -> MalType:
    if isinstance(a, MalNil):
        return MalNil()
    if a.value:
        return a[0]
    else:
        return MalNil()


def rest(a: MalList | MalVector | MalNil) -> MalList:
    if isinstance(a, MalNil) or len(a.value) < 2:
        return MalList()
    else:
        return MalList(a.value[1:])


def is_macro(a: MalFnTCO) -> MalBoolean:
    return malBool(a.is_macro)


def throw(a: MalType) -> MalType:
    raise MalError(a)


def apply(a: MalFn | MalFnTCO, *b: MalType) -> MalType:
    match b[-1]:
        case MalList() | MalVector():
            return a(*(list(b[:-1]) + b[-1].value))
        case _:
            return a(*list(b))


def map(a: MalFn | MalFnTCO, b: MalList | MalVector) -> MalList:
    out = MalList()
    for el in b.value:
        out.append(a(el))
    return out


def assoc(a: MalMap, *b: MalType) -> MalMap:
    return MalMap({key: a[key] for key in a.value}).from_list(*b)


def dissoc(a: MalMap, *b: MalType) -> MalMap:
    out = MalMap({key: a[key] for key in a.value})
    for arg in b:
        out.value.pop(arg, None)
    return out


def get(a: MalMap | MalNil, b: MalType) -> MalType:
    if isinstance(a, MalMap) and b in a:
        return a[b]
    return MalNil()


def contains(a: MalMap, b: MalType) -> MalBoolean:
    return malBool(b in a)


def keys(a: MalMap) -> MalList:
    return MalList(a.value.keys())


def values(a: MalMap) -> MalList:
    return MalList(a.value.values())


def is_t(t: type, a: MalType) -> MalBoolean:
    return malBool(isinstance(a, t))


def as_t(t: type, a: MalType) -> MalType:
    return t(a.value)


def readline(a: MalString) -> MalString | MalNil:
    try:
        return MalString(input(a.value))
    except EOFError:
        return MalNil()


def meta(a: hasMeta) -> MalType:
    return a.meta


def with_meta(a: hasMeta, b: MalType) -> hasMeta:
    match a:
        case MalList():
            out = MalList(a.value)
        case MalVector():
            out = MalVector(a.value)
        case MalMap():
            out = MalMap({k: a[k] for k in a})
        case MalFn():
            out = MalFn(a.fn)
        case MalFnTCO():
            out = MalFnTCO(a.ast, a.params, a.env, a.fn)
            out.is_macro = a.is_macro
    out.meta = b
    return out


def time_ms() -> MalNumber:
    return MalNumber(time.time_ns() // 1000)


def conj(a: MalSequence, *b: MalType) -> MalSequence:
    match a:
        case MalList():
            return MalList(list(b)[::-1] + a.value)
        case MalVector():
            return MalVector(a.value + list(b))
        case _:
            raise TypeError("Invalid input to conj", a)


def seq(a: MalSequence | MalString | MalNil) -> MalList | MalNil:
    match a:
        case MalList([]):
            return MalNil()
        case MalVector([]):
            return MalNil()
        case MalString(""):
            return MalNil()
        case MalNil():
            return MalNil()
        case MalList():
            return a
        case MalVector(value):
            return MalList(value)
        case MalString(value):
            return MalList(list(value))
        case _:
            raise TypeError("Invalid input to seq", a)


def synpy_eval(a: MalString) -> MalType:
    result = eval(a.value)
    return to_mal_type(result)


ns: dict[str, Fn] = {
    # numeric functions
    "+": add,
    "-": sub,
    "*": mul,
    "/": div,
    # comparisons
    "=": eq,
    "<": lt,
    "<=": le,
    ">": gt,
    ">=": ge,
    # string functions
    "prn": prn,
    "pr-str": pr_str_,
    "str": str_,
    "println": println,
    "read-string": read_string,
    "slurp": slurp,
    "readline": readline,
    # sequence functions
    "count": count,
    "cons": cons,
    "concat": concat,
    "vec": vec,
    "nth": nth,
    "first": first,
    "rest": rest,
    "empty?": is_empty,
    "seq": seq,
    # map functions
    "assoc": assoc,
    "dissoc": dissoc,
    "get": get,
    "contains?": contains,
    "keys": keys,
    "vals": values,
    # atom functions
    "deref": deref,
    "swap!": swap,
    "reset!": reset,
    # function functions
    "apply": apply,
    "map": map,
    "macro?": is_macro,
    # is_t
    "list?": lambda a: is_t(MalList, a),
    "atom?": lambda a: is_t(MalAtom, a),
    "nil?": lambda a: is_t(MalNil, a),
    "true?": lambda a: is_t(MalTrue, a),
    "false?": lambda a: is_t(MalFalse, a),
    "symbol?": lambda a: is_t(MalSymbol, a),
    "keyword?": lambda a: is_t(MalKeyword, a),
    "vector?": lambda a: is_t(MalVector, a),
    "sequential?": lambda a: is_t(MalSequence, a),
    "map?": lambda a: is_t(MalMap, a),
    "string?": lambda a: is_t(MalString, a),
    "number?": lambda a: is_t(MalNumber, a),
    "fn?": lambda a: malBool(is_t(MalFn, a) or is_t(MalFnTCO, a)),
    # as_t
    "list": lambda *a: as_t(MalList, MalList(a)),
    "atom": lambda a: as_t(MalAtom, a),
    "symbol": lambda a: as_t(MalSymbol, a),
    "keyword": lambda a: MalKeyword(":" + a.value),
    "vector": lambda *a: as_t(MalVector, MalList(a)),
    "hash-map": lambda *a: MalMap().from_list(*a),
    # meta
    "meta": meta,
    "with-meta": with_meta,
    # other
    "throw": throw,
    "time-ms": time_ms,
    "synpy-eval": synpy_eval,
}
