import re
import logging
from typing import Callable

logger = logging.getLogger(__name__)


class MalType:
    value: str | int | list | Callable

    __match_args__ = ("value",)

    def __str__(self, readably=False) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"{type(self)}({repr(self.value)})"

    def __eq__(self, other) -> bool:
        return self.value == other.value

    def __bool__(self) -> bool:
        return True


class MalSequence(MalType):
    value: list[MalType] = []
    start: str = ""
    end: str = ""

    def __init__(self, *args):
        if args and len(args) == 1:
            self.value: list[MalType] = args[0]
        elif args:
            raise TypeError(f"Too many arguments {args}")
        else:
            self.value = []

    def __str__(self, readably=False) -> str:
        # logger.info(self.value)
        return (
            self.start
            + " ".join([x.__str__(readably=readably) for x in self.value])
            + self.end
        )

    def append(self, item: MalType) -> None:
        self.value.append(item)

    def __contains__(self, key) -> bool:
        return key in self.value

    def __getitem__(self, key) -> MalType:
        return self.value[key]

    def __len__(self) -> int:
        return len(self.value)


class MalList(MalSequence):
    start = "("
    end = ")"


class MalVector(MalSequence):
    start = "["
    end = "]"


class MalMap(MalType):
    def __init__(self, *args):
        if args and len(args) == 1:
            logger.info(args)
            self.value: dict[MalType, MalType] = args[0]
        elif args:
            raise TypeError(f"Too many arguments {args}")
        else:
            self.value = {}

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


class MalNumber(MalType):
    def __init__(self, value: int):
        self.value = value

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
        self.value: str = self.parse(value)

    def parse(self, value: str) -> str:
        return re.sub(
            r"\\.", lambda m: self.ESCAPE[m.string[m.start() : m.end()]], value
        )

    def escape(self, value: str) -> str:
        return re.sub(
            r'"|\n|\\', lambda m: self.PARSE[m.string[m.start() : m.end()]], value
        )

    def __str__(self, readably=False) -> str:
        if readably:
            out = self.escape(self.value)
        else:
            out = self.value
        return '"' + out + '"'

    def __len__(self) -> int:
        return len(self.value)

    def __hash__(self) -> int:
        return hash('"' + self.value)


class MalNil(MalType):
    value = "nil"

    def __bool__(self) -> bool:
        return False


class MalBoolean(MalType):
    pass


class MalTrue(MalBoolean):
    value = "true"


class MalFalse(MalBoolean):
    value = "false"

    def __bool__(self) -> bool:
        return False


class MalFn(MalType):
    def __init__(self, value: Callable):
        self.value: Callable = value

    def __call__(self, *args, **kwargs):
        return self.value(*args, **kwargs)


class EOFError_(Exception):
    pass
