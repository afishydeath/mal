from types_ import MalType
import reader
import printer


def READ(string: str) -> MalType:
    return reader.read_str(string)


def EVAL(ast: MalType, env) -> MalType:
    return ast


def PRINT(exp: MalType) -> str:
    return printer.pr_str(exp)


def rep(string):
    return PRINT(EVAL(READ(string), ""))


if __name__ == "__main__":
    while True:
        print(rep(input("user> ")))
