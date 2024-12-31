from re import findall
from m_types import MalType, MalList, MalSymbol, MalNumber

class Reader:
    def __init__(self, tokens : list[str]) -> None:
        self.tokens : list[str] = tokens
        self.position : int = 0
    def next(self) -> str:
        self.position += 1
        return self.tokens[self.position-1]
    def peek(self) -> str:
        return self.tokens[self.position]

def read_str(string : str) -> MalType:
    tokens = tokenize(string)
    reader = Reader(tokens)
    mals = read_form(reader)
    return mals

def tokenize(string : str) -> list[str]:
    pattern = r"""[\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"?|;.*|[^\s\[\]{}('"`,;)]*)"""
    tokens = findall(pattern, string)
    return tokens

def read_form(reader : Reader) -> MalType:
    first = reader.peek()
    match first:
        case '(' :
            return read_list(reader)
        case _ :
            return read_atom(reader)

def read_list(reader : Reader) -> MalList:
    mals : MalList = MalList()
    reader.next()
    to_add = read_form(reader)
    while to_add != MalSymbol(')'):
        mals.append(to_add)
        to_add = read_form(reader)
    return mals

def read_atom(reader : Reader) -> MalType:
    next = reader.next()
    if next.isnumeric():
        return MalNumber(next)
    else:
        return MalSymbol(next)
