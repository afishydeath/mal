import re
from typing import Iterator, List
from re import Match, Pattern
from m_types import (
    List_,
    Form,
    String,
    Symbol,
    Number,
    Nil,
    Boolean,
    Keyword,
    Vector,
    Map,
)
from errors import m_EOFError

tokens = (
    r"(?P<whitespace>(?:[\s,]|;[^\n\r]*)+)"
    + "|"
    + r'(?P<string>"(?:(?:[^"\\]|\\.)*")?)'
    + "|"
    + r"(?P<list_start>\()"
    + "|"
    + r"(?P<vector_start>\[)"
    + "|"
    + r"(?P<map_start>\{)"
    + "|"
    + r"(?P<macro>['`@]|~@?)"
    + "|"
    + r"(?P<meta>\^)"
    + "|"
    + r"(?P<close_bracket>[])}])"
    + "|"
    + r"(?P<number>-?\d+)"
    + "|"
    + r"""(?P<symbol>[^]\s"'(),;@[^`{}~]+)"""
)
pattern: Pattern = re.compile(tokens)


class Reader:
    def __init__(self, tokens: Iterator[Match[str]]) -> None:
        self._tokens = (token for token in tokens if token.lastgroup != "whitespace")
        try:
            self._next: Match[str] | None = next(self._tokens)
        except StopIteration:
            self._next = None

    def peek(self) -> Match[str] | None:
        return self._next

    def next(self) -> Match[str] | None:
        old = self._next
        try:
            self._next = next(self._tokens)
        except StopIteration:
            self._next = None
        return old


def read_str(text: str) -> Form | None:
    tokens = tokenize(text)
    reader = Reader(tokens)
    ast = read_form(reader)
    return ast


def tokenize(text: str) -> Iterator[Match[str]]:
    return pattern.finditer(text)


def read_form(reader: Reader) -> Form | None:
    if first := reader.peek():
        match first.string[first.start() : first.end()]:
            case "(":
                return read_list(reader)
            case "[":
                return read_vec(reader)
            case "{":
                return read_map(reader)
            case _:
                return read_atom(reader)


def read_sequential(reader: Reader, end: str) -> List[Form]:
    reader.next()
    contents: List[Form] = []
    while (next := reader.peek()) and next.string[next.start() : next.end()] != end:
        if (to_add := read_form(reader)) is not None:
            contents.append(to_add)
    if next:
        reader.next()
        return contents
    raise m_EOFError("eof while parseing sequential")


def read_list(reader: Reader) -> List_:
    return List_(read_sequential(reader, ")"))


def read_vec(reader: Reader) -> Vector:
    return Vector(read_sequential(reader, "]"))


def read_map(reader: Reader) -> Map:
    return Map().from_list(read_sequential(reader, "}"))


escapes = {"\\\\": "\\", '\\"': '"', "\\n": "\n"}


def unescape(text: str) -> str:
    return re.sub(r"\\.", lambda x: escapes[x.string[x.start() : x.end()]], text)


macros = {
    "'": "quote",
    "`": "quasiquote",
    "@": "deref",
    "~": "unquote",
    "~@": "splice-unquote",
}


def read_atom(reader: Reader) -> Form | None:
    next = reader.next()
    if next is None:
        return None
    start, end = next.span()
    text: str = next.string[start:end]
    match next.lastgroup:
        case "whitespace":
            return None
        case "string":
            if end - start == 1:
                raise m_EOFError("eof while parseing string")
            return String(unescape(text))
        case "macro":
            if (quoted := read_form(reader)) is not None:
                return List_([Symbol(macros[text]), quoted])
            else:
                raise Exception("quoted missing")
        case "meta":
            if (meta := read_form(reader)) is not None and (
                content := read_form(reader)
            ) is not None:
                return List_([Symbol("with-meta"), content, meta])
            else:
                raise Exception("with meta failed")
        case "number":
            return Number(text)
        case "symbol":
            match text:
                case "nil":
                    return Nil.NIL
                case "true":
                    return Boolean.TRUE
                case "false":
                    return Boolean.FALSE
                case _:
                    if text.startswith(":"):
                        return Keyword(text[1:])
                    return Symbol(text)
        case x:
            raise Exception(f"unhandled match group {x}")
