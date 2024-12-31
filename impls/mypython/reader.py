from re import findall
from m_types import MalBoolean, MalEmptyReturn, MalListOrEmpty, MalNil, MalType, MalList, MalSymbol, MalNumber

class Reader:
    def __init__(self, tokens : list[str]) -> None:
        self.tokens : list[str] = tokens
        self.position : int = 0
    def next(self) -> str:
        self.position += 1
        if self.position < len(self.tokens):
            return self.tokens[self.position-1]
        else:
            return 'EOF'
    def peek(self) -> str:
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        else:
            return 'EOF'

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
            return read_list(reader, '(')
        case '[':
            return read_list(reader, '[')
        case _ :
            return read_atom(reader)

def read_list(reader : Reader, startBracket : str) -> MalListOrEmpty:
    mals : MalList = MalList()
    end_character : MalSymbol = MalSymbol(')')
    if startBracket == '[':
        end_character = MalSymbol(']')
        mals.make_vector()
    reader.next()
    to_add = read_form(reader)
    while to_add != end_character:
        if to_add == MalSymbol('EOF'):
            eof_out = MalList([to_add])
            if startBracket == '[':
                eof_out.make_vector()
            return eof_out
        if to_add != MalEmptyReturn:
            mals.append(to_add)
        to_add = read_form(reader)
    if mals != MalList():
        return mals
    else:
        return MalEmptyReturn

def read_atom(reader : Reader) -> MalType:
    next = reader.next()
    if next.isnumeric():
        return MalNumber(next)
    elif next == 'true':
        return MalBoolean(True)
    elif next == 'false':
        return MalBoolean(True)
    elif next == 'nil':
        return MalNil
    elif next[0]==';':
        return MalEmptyReturn
    else:
        return MalSymbol(next)
