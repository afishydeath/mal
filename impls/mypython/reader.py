#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p python312 python312Packages.regex
import regex as re

class Reader:
    def __init__(self, tokens):
        self.pos = 0
        self.tokens = tokens

    def peek(self):
        return self.tokens[self.pos]

    def next(self):
        out = self.peek()
        self.pos+=1
        return out

def tokenize(string):
    tokens = re.findall(R'[\s,]*(~@|[\[\]{}()\'`~^@]|"(?:\\.|[^\\"])*"?|;.*|[^\s\[\]{}(\'"`,;)]*)', string)
    return tokens

def read_form(reader):
    if reader.peek()[0] == '(':
        return read_list(reader)
    else:
        return read_atom(reader)


def read_list(reader):
    mals = []
    reader.next()
    while reader.peek() != ')':
        if reader.peek() == '':
            return 'EOF'
        mals.append(read_form(reader))
    return mals

def read_atom(reader):
    token = reader.next()
    if token.isdigit():
        return int(token)
    elif token in [i for i in '+-*/']:
        return token
    else:
        return token #TODO

def read_str(string):
    tokens = tokenize(string)
    reader = Reader(tokens)
    mal = read_form(reader)
    return mal

if __name__ == "__main__":
    print(read_str("[1 2"))
