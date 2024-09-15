#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p python312 python312Packages.regex
import regex as re
import mal_readline
from mal_types import MalType, MalList, MalSymbol, MalInteger

class Reader:
    def __init__(self, tokens:list[str]) -> None:
        self.pos = 0
        self.tokens = tokens

    def peek(self) -> str:
        return self.tokens[self.pos]

    def next(self) -> str:
        out = self.peek()
        self.pos+=1
        return out

def tokenize(string:str) -> list[str]:
    tokens = re.findall(R'[\s,]*(~@|[\[\]{}()\'`~^@]|"(?:\\.|[^\\"])*"?|;.*|[^\s\[\]{}(\'"`,;)]*)', string)
    return tokens

def read_form(reader:Reader) -> MalType:
    if reader.peek() == '(':
        return read_list(reader)
    else:
        return read_atom(reader)


def read_list(reader:Reader) -> MalList:
    mals = MalList([])
    while True:
        reader.next()
        if reader.peek() == ')':
            return mals
        elif reader.peek() == '':
            mals.append(MalSymbol("EOF"))
            return mals
        else:
            mals.append(read_form(reader))

def read_atom(reader:Reader) -> MalType:
    token = reader.peek()
    if token.isdigit():
        return MalInteger(int(token))
    else:
        return MalSymbol(token)

def read_str(string:str) -> MalType:
    tokens = tokenize(string)
    reader = Reader(tokens)
    ast = read_form(reader)
    return ast

if __name__ == "__main__":
    string = mal_readline.input_("user> ")
    print(string)
    tokens = tokenize(string)
    print(tokens)
    reader = Reader(tokens)
    ast = read_form(reader)
    print(ast)
