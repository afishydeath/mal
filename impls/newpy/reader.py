from types_ import (
    MalString,
    MalType,
    MalList,
    MalNumber,
    MalSymbol,
    MalTrue,
    MalFalse,
    MalNil,
    MalVector,
    MalMap,
    MalKeyword,
    EOFError_,
)
import re
import logging

logger = logging.getLogger(__name__)

token_pattern = re.compile(
    r"""[\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"?|;.*|[^\s\[\]{}('"`,;)]*)"""
)
atom_pattern = re.compile(
    "|".join(
        [
            r"""(?P<int>-?\d+)""",
            r"""(?P<true>true)""",
            r"""(?P<false>false)""",
            r"""(?P<nil>nil)""",
            r"""(?P<goodstring>"(?:\\.|[^\\"])*")""",
            r"""(?P<badstring>"(?:\\.|[^\\"])*)""",
            r"""(?P<macro>~@|['`~@])""",
            r"""(?P<meta>\^)""",
            r"""(?P<keyword>:.*)""",
            r"""(?P<symbol>.*)""",
        ]
    )
)


class Reader:
    def __init__(self, tokens: list[str]):
        self.tokens = tokens
        self.position = 0

    def next(self) -> str:
        out = self.peek()
        self.position += 1
        return out

    def peek(self) -> str:
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        else:
            raise EOFError_(f"EOF no more tokens{str(self)}")

    def __str__(self):
        return f"{self.tokens=}, {self.position=}"


def read_str(string: str) -> MalType:
    tokens = tokenise(string)
    reader = Reader(tokens)
    return read_form(reader)


def tokenise(string) -> list:
    tokens = []
    for token in token_pattern.findall(string):
        if token:
            tokens.append(token)
    return tokens


def read_form(reader: Reader) -> MalType:
    # logger.info(reader)
    peek = reader.peek()
    if peek[0] in ("(", "[", "{"):
        return read_list(reader, peek[0])
    else:
        return read_atom(reader)


END = {"(": ")", "[": "]", "{": "}"}
TYPE = {"(": MalList, "[": MalVector, "{": MalMap}


def read_list(reader: Reader, start: str) -> MalList:
    reader.next()
    running = TYPE[start]()
    tok = read_form(reader)
    map = start == "{"
    if map:
        key_flag = True
        key: MalType = MalNil()
    while tok != MalSymbol(END[start]):
        if map:
            if key_flag:
                key_flag = False
                key = tok
            else:
                key_flag = True
                running[key] = tok
        else:
            running.append(tok)
        tok = read_form(reader)
    if map and not key_flag:
        raise EOFError_(f"EOF unmatched key value in map {running}")
    return running


MACROS = {
    "'": "quote",
    "`": "quasiquote",
    "~": "unquote",
    "~@": "splice-unquote",
    "@": "deref",
}


def read_atom(reader: Reader) -> MalType:
    token = reader.next()
    # logger.info(token)
    m = atom_pattern.fullmatch(token)
    # logger.info(m)
    if not m:
        raise Exception(f"atom match failed on {token}")

    match m.lastgroup:
        case "int":
            return MalNumber(int(token))
        case "true":
            return MalTrue()
        case "false":
            return MalFalse()
        case "nil":
            return MalNil()
        case "goodstring":
            s = MalString(MalString("").parse(token[1:-1]))
            logger.info(s)
            return s
        case "badstring":
            raise EOFError_(f"EOF unclosed string at {token}")
        case "macro":
            return MalList([MalSymbol(MACROS[token]), read_form(reader)])
        case "meta":
            meta = read_form(reader)
            block = read_form(reader)
            return MalList([MalSymbol("with-meta"), block, meta])
        case "keyword":
            return MalKeyword(token)
        case "symbol":
            # logger.info(token)
            return MalSymbol(token)
        case _:
            raise Exception(f"atom matched pattern, but had no group on {token}")
