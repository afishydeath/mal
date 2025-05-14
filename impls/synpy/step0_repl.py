def READ(string):
    return string


def EVAL(ast, env):
    return ast


def PRINT(exp):
    return exp


def rep(string):
    return PRINT(EVAL(READ(string), ""))


if __name__ == "__main__":
    while True:
        print(rep(input("user> ")))
