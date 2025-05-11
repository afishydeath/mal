from types_ import MalType, MalList, MalNumber, MalSymbol
import re

token_pattern = re.compile(
    r"""[\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"?|;.*|[^\s\[\]{}('"`,;)]*)"""
)
atom_pattern = re.compile(
    (
        r"""(?P<int>-\d+)"""
        "|"
        r"""(?P<symbol>.*)"""
    )
)


class Reader:
    def __init__(self, tokens: list[str]):
        self.tokens = tokens
        self.position = 0

    def next(self) -> str:
        self.position += 1
        return self.peek()

    def peek(self) -> str:
        if self.position <= len(self.tokens):
            return self.tokens[self.position - 1]
        else:
            raise EOFError("End of tokens")


def read_str(string: str) -> MalType:
    # print(string)
    tokens = tokenise(string)
    # print(tokens)
    reader = Reader(tokens)
    return read_form(reader)


def tokenise(string) -> list:
    return token_pattern.findall(string)[:-1]


def read_form(reader: Reader) -> MalType:
    peek = reader.peek()
    match peek[0]:
        case "(":
            return read_list(reader)
        case _:
            return read_atom(reader)


def read_list(reader: Reader) -> MalList:
    reader.next()
    running_list = MalList([])
    while (tok := read_form(reader)) != ")":
        running_list.append(tok)
    return running_list


def read_atom(reader: Reader):
    token = reader.next()
    m = atom_pattern.fullmatch(token)
    if not m:
        raise Exception(f"atom match failed on {token}")

    match m.lastgroup:
        case "int":
            return MalNumber(int(token))
        case "symbol":
            return MalSymbol(token)
        case _:
            raise Exception(f"atom matched pattern, but had no group on {token}")
