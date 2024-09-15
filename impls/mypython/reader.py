#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p python312 python312Packages.regex
import regex as re
import mal_readline
from mal_types import MalType, Number, List, Symbol
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


def read_list(reader:Reader) -> List:
    mals = []
    while True:
        reader.next()
        if reader.peek() == ')':
            return List(mals)
        elif reader.peek() == '':
            mals.append(Symbol("EOF"))
            return List(mals)
        else:
            mals.append(read_form(reader))

def read_atom(reader:Reader) -> MalType:
    token = reader.peek()
    if token.isdigit() or (token[0]=='-' and token[1:].isdigit()):
        return Number(int(token))
    else:
        return Symbol(token)

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
