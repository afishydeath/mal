def READ(*args):
    return args[0]

def EVAL(*args):
    return args[0]

def PRINT(*args):
    return args[0]

def rep(*args):
    return READ(EVAL(PRINT(args[0])))

def main():
    try:
        print(rep(input("user> ")))
    except EOFError:
        return 0
    while True:
        try:
            print(rep(input("user> ")))
        except EOFError:
            return 0

if __name__ == "__main__":
    main()
