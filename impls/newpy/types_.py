import re
import logging

logger = logging.getLogger(__name__)


class MalType:
    value: str | int | list | None = None

    def __str__(self, readably=False):
        return str(self.value)

    def __repr__(self):
        return f"{type(self)}({repr(self.value)})"

    def __eq__(self, other):
        return self.value == other.value


class MalSequence(MalType):
    value: list[MalType] = []
    start: str = ""
    end: str = ""

    def __str__(self, readably=False):
        # logger.info(self.value)
        return (
            self.start
            + " ".join([x.__str__(readably=readably) for x in self.value])
            + self.end
        )


class MalList(MalSequence):
    start = "("
    end = ")"

    def __init__(self, value: list[MalType]):
        self.value: list[MalType] = value

    def append(self, item: MalType):
        self.value.append(item)


class MalVector(MalSequence):
    start = "["
    end = "]"

    def __init__(self, value: list[MalType]):
        self.value: list[MalType] = value

    def append(self, item: MalType):
        self.value.append(item)


class MalMap(MalSequence):
    start = "{"
    end = "}"

    def __init__(self, value: list[MalType]):
        self.value: list[MalType] = value

    def append(self, item: MalType):
        self.value.append(item)


class MalNumber(MalType):
    def __init__(self, value: int):
        self.value = value


class MalSymbol(MalType):
    def __init__(self, value: str):
        self.value = value


class MalKeyword(MalType):
    def __init__(self, value: str):
        self.value: str = value[1:]

    def __str__(self, readably=False):
        return ":" + self.value


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

    def __str__(self, readably=False):
        if readably:
            out = self.escape(self.value)
        else:
            out = self.value
        return '"' + out + '"'


class MalNil(MalType):
    value = "nil"


class MalBoolean(MalType):
    pass


class MalTrue(MalBoolean):
    value = "true"


class MalFalse(MalBoolean):
    value = "false"


class EOFError_(Exception):
    pass
