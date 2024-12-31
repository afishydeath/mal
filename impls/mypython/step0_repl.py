def READ(*args):
    return args[0]

def EVAL(*args):
    return args[0]

def PRINT(*args):
    return args[0]

def rep(*args):
    return READ(EVAL(PRINT(*args[0])))

if __name__ == "__main__":
    while True:
        try:
            inp = input("user> ")
        except EOFError:
            break
        print(rep(inp))
