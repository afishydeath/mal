import re
import logging
from collections.abc import Iterable
from typing import Protocol

logger = logging.getLogger(__name__)


class MalType:
    value = "notimplemented"

    __match_args__ = ("value",)

    def __str__(self, readably=False) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"{type(self)}({repr(self.value)})"

    def __eq__(self, other) -> bool:
        return self.value == other.value and self.__class__ == other.__class__

    def __lt__(self, other) -> bool:
        return self.value < other.value

    def __le__(self, other) -> bool:
        return self.value <= other.value

    def __gt__(self, other) -> bool:
        return self.value > other.value

    def __ge__(self, other) -> bool:
        return self.value >= other.value

    def __bool__(self) -> bool:
        return True


class MalNil(MalType):
    value = "nil"

    def __bool__(self) -> bool:
        return False

    def __len__(self) -> int:
        return 0


class MalSequence[T: MalType](MalType):
    value: list[T] = []
    start: str = ""
    end: str = ""
    meta: MalType = MalNil()

    def __init__(self, *args: Iterable[T]):
        # logger.info(args)
        if args and len(args) == 1:
            self.value: list[T] = list(args[0])
        elif args:
            raise TypeError(f"Too many arguments {args}")
        else:
            self.value = []

    def __str__(self, readably=False) -> str:
        return (
            self.start
            + " ".join([x.__str__(readably=readably) for x in self.value])
            + self.end
        )

    def append(self, item: T) -> None:
        self.value.append(item)

    def __contains__(self, key) -> bool:
        return key in self.value

    def __iter__(self):
        return iter(self.value)

    def __getitem__(self, key: int) -> T:
        # logger.info("here")
        try:
            return self.value[key]
        except IndexError:
            raise MalIndexError(key)

    def __len__(self) -> int:
        return len(self.value)

    def __eq__(self, other) -> bool:
        return self.value == other.value


class MalList[T: MalType](MalSequence):
    value: list[T]
    start = "("
    end = ")"


class MalVector[T: MalType](MalSequence):
    value: list[T]
    start = "["
    end = "]"


class MalMap(MalType):
    meta: MalType = MalNil()

    def __init__(self, *args: dict[MalType, MalType]):
        if args and len(args) == 1:
            # logger.info(args)
            self.value: dict[MalType, MalType] = args[0]
        elif args:
            raise TypeError(f"Too many arguments {args}")
        else:
            self.value = {}

    def from_list(self, *args: MalType) -> "MalMap":
        keyflag = True
        key: MalType = MalNil()
        for arg in args:
            if keyflag:
                key = arg
                keyflag = False
            else:
                self[key] = arg
                keyflag = True
        if not keyflag:
            raise KeyError(f"Uneven arguments provided {args}")
        return self

    def __setitem__(self, key, value) -> None:
        self.value[key] = value

    def __getitem__(self, key) -> MalType:
        return self.value[key]

    def __contains__(self, key) -> bool:
        return key in self.value

    def __len__(self) -> int:
        return len(self.value)

    def __str__(self, readably=False) -> str:
        return (
            "{"
            + " ".join(
                [
                    " ".join([y.__str__(readably=readably) for y in x])
                    for x in self.value.items()
                ]
            )
            + "}"
        )

    def __iter__(self):
        return iter(self.value)


class MalNumber(MalType):
    def __init__(self, value: int):
        self.value: int = value

    def __add__(self, other):
        return MalNumber(self.value + other.value)

    def __sub__(self, other):
        return MalNumber(self.value - other.value)

    def __mul__(self, other):
        return MalNumber(self.value * other.value)

    def __floordiv__(self, other):
        return MalNumber(self.value // other.value)


class MalSymbol(MalType):
    def __init__(self, value: str):
        self.value = value

    def __hash__(self) -> int:
        return hash(self.value)


class MalKeyword(MalType):
    def __init__(self, value: str):
        self.value: str = value[1:]

    def __str__(self, readably=False) -> str:
        return ":" + self.value

    def __hash__(self) -> int:
        return hash(":" + self.value)


class MalString(MalType):
    ESCAPE = {'\\"': '"', "\\n": "\n", "\\\\": "\\"}
    PARSE = {'"': '\\"', "\n": "\\n", "\\": "\\\\"}

    def __init__(self, value: str):
        self.value: str = value

    def parse(self, value: str) -> str:
        return re.sub(r"\\.", lambda m: self.ESCAPE[m.group()], value)

    def escape(self, value: str) -> str:
        return re.sub(r'["\n\\]', lambda m: self.PARSE[m.group()], value)

    def __str__(self, readably=False) -> str:
        if readably:
            return '"' + self.escape(self.value) + '"'
        else:
            return self.value

    def __len__(self) -> int:
        return len(self.value)

    def __hash__(self) -> int:
        return hash('"' + self.value)


class MalBoolean(MalType):
    pass


class MalTrue(MalBoolean):
    value = "true"


class MalFalse(MalBoolean):
    value = "false"

    def __bool__(self) -> bool:
        return False


def malBool(cond) -> MalBoolean:
    return MalTrue() if cond else MalFalse()


class Fn0Arg[T: MalType](Protocol):
    def __call__(self) -> T: ...


class Fn1Arg[T: MalType, T1: MalType](Protocol):
    def __call__(self, a: T) -> T1: ...


class Fn2Arg[T: MalType, T1: MalType, T2: MalType](Protocol):
    def __call__(self, a: T, b: T1) -> T2: ...


class FnXArg[T: MalType, T1: MalType](Protocol):
    def __call__(self, *a: T) -> T1: ...


class FnHeadXTail[T: MalType, T1: MalType, T2: MalType, T3: MalType](Protocol):
    def __call__(self, a: T, *b: T1, c: T2) -> T3: ...


Fn = Fn0Arg | Fn1Arg | Fn2Arg | FnXArg | FnHeadXTail


class MalFn(MalType):
    meta: MalType = MalNil()

    def __init__(self, value: Fn):
        self.value = "#<function>"
        self.fn: Fn = value

    def __call__(self, *args: MalType) -> MalType:
        logger.info(args)
        return self.fn(*args)  # type: ignore // this is literally a broken error i do not get it

    def __str__(self, readably=False):
        return self.value


class MalFnTCO(MalType):
    meta: MalType = MalNil()

    def __init__(self, ast: MalType, params: MalList[MalSymbol], env, fn: MalFn):
        self.value = "#<functionwithtco>"
        self.is_macro = False
        self.ast: MalType = ast
        self.params: MalList[MalSymbol] = params
        self.env = env
        self.fn: MalFn = fn

    def __call__(self, *args: MalType) -> MalType:
        return self.fn(*args)

    def __str__(self, readably=False):
        return self.value


hasMeta = MalSequence | MalMap | MalFn | MalFnTCO


def to_mal_type(value) -> MalType:
    match value:
        case list() | tuple():
            return MalList([to_mal_type(x) for x in value])
        case dict():
            return MalMap({to_mal_type(k): to_mal_type(value[k]) for k in value})
        case str():
            return MalString(value)
        case int():
            return MalNumber(value)
        case bool():
            return malBool(value)
        case _:
            raise TypeError(
                f"type {type(value)} not implemented for 'to_mal_type' for {value}"
            )


class MalAtom(MalType):
    def __init__(self, value: MalType):
        self.value: MalType = value

    def __str__(self, readably=False):
        return MalList([MalSymbol("atom"), self.value]).__str__(readably=readably)


class MalError(Exception):
    prefix = ""
    postfix = ""

    def __init__(self, value):
        # logger.info(repr(value))
        self.value = str(value)
        self.ast = None
        if isinstance(value, MalType) and self.__class__ == MalError:
            self.ast = value

    def __str__(self) -> str:
        return (
            (self.prefix + " " if self.prefix else "")
            + self.value
            + (" " + self.postfix if self.postfix else "")
        )


class MalKeyError(MalError):
    postfix = "not found"


class MalIndexError(MalError):
    prefix = "Index out of range:"


class MalEofError(MalError):
    prefix = "EOF:"
