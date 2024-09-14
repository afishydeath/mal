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
    match reader.peek()[0]:
        case '(':
            return read_list(reader)
        case _ :
            return read_atom(reader)

def read_list(reader):
    mals = []
    reader.next()
    while reader.peek() != ')':
        mals.append(read_form(reader))
    return mals

def read_atom(reader):
    token = reader.next()
    if token.isdigit():
        return int(token)
    elif token in [i for i in '+-*/']:
        return token
    else:
        print("error, "+token)

def read_str(string):
    tokens = tokenize(string)
    reader = Reader(tokens)
    mal = read_form(reader)
    return mal

# if __name__ == "__main__":
#     print(read_str("(+ 2 (* 3 4))"))
