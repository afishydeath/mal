import reader, printer

def READ(string):
    return reader.read_str(string)

def EVAL(mals):
    return mals

def PRINT(mals):
    print(mals)
    return printer.pr_str(mals)

def rep(string):
    mals = READ(string)
    mals = EVAL(mals)
    return PRINT(mals)

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
