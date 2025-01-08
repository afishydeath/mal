from re import findall
import re
from m_types import MalEmptyExpr, MalType, MalEOFError, MalSequential, MalList, MalVector, MalHashMap, MalString, MalNumber, MalSymbol, MalKeyword, MalNil, MalBoolean

class Reader:
    def __init__(self, tokens : list[str]) -> None:
        self.tokens : list[str] = tokens
        self.position : int = 0
    def next(self) -> str:
        self.position += 1
        if self.position < len(self.tokens):
            return self.tokens[self.position-1]
        else:
            raise MalEOFError
    def peek(self) -> str:
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        else:
            raise MalEOFError

def read_str(string : str) -> MalType:
    tokens = tokenize(string)
    if len(tokens) == 0:
        raise MalEmptyExpr
    reader = Reader(tokens)
    mals = read_form(reader)
    return mals

def tokenize(string : str) -> list[str]:
    pattern = r"""[\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"?|;.*|[^\s\[\]{}('"`,;)]*)"""
    tokens = findall(pattern, string)
    return tokens

def read_form(reader : Reader) -> MalType:
    first = reader.peek()
    if first in ['(', '[']:
        return read_list(reader, first)
    elif first == '{':
        return read_hash_map(reader)
    else:
        return read_atom(reader)

def read_list(reader : Reader, startBracket : str) -> MalSequential:
    mals : MalSequential = MalSequential()
    match startBracket:
        case '(':
            end_character : MalSymbol = MalSymbol(')')
            mals = MalList()
        case '[':
            end_character : MalSymbol = MalSymbol(']')
            mals = MalVector()
        case _:
            raise Exception("unreachable")
    reader.next()
    to_add : MalType = read_form(reader)
    while to_add != end_character:
        mals.append(to_add)
        to_add = read_form(reader)
    return mals

def read_hash_map(reader: Reader) -> MalHashMap:
    end_character : MalSymbol = MalSymbol('}')
    mals : MalHashMap = MalHashMap()
    reader.next()
    even : bool = True
    to_add : MalType = MalNil()
    key : MalType = MalNil()
    value : MalType = MalNil()
    while to_add != end_character:
        to_add = read_form(reader)
        if even:
            key = to_add
            even = False
        else:
            value = to_add
            mals[key] = value
            even = True
    if even:
        raise MalEOFError
    else:
        return mals

def read_atom(reader : Reader) -> MalType:
    next = reader.next()
    if next.isnumeric():
        return MalNumber(next)
    elif next == 'true':
        return MalBoolean(True)
    elif next == 'false':
        return MalBoolean(False)
    elif next == 'nil':
        return MalNil()
    elif next[0]==':':
        return MalKeyword(next[1:])
    elif next[0]=='"':
        pattern = r'"(?:[^\\\n]|\\\\|\\"|\\n)*"'
        if re.match(pattern,next):
            return MalString(next[1:-1])
        else:
            raise MalEOFError
    else:
        return MalSymbol(next)
