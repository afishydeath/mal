from m_readline import m_input
from m_types import (
    MalEOFError,
    MalEmptyExpr,
    MalFalse,
    MalHashMap,
    MalList,
    MalNil,
    MalNotFound,
    MalNumber,
    MalSymbol,
    MalType,
    MalVector,
)
import reader
import printer

repl_env = {
    "+": lambda a, b: MalNumber(a + b),
    "-": lambda a, b: MalNumber(a - b),
    "*": lambda a, b: MalNumber(a * b),
    "/": lambda a, b: MalNumber(a / b),
}


def READ(string: str) -> MalType:
    return reader.read_str(string)


def EVAL(ast: MalType, repl_env):
    debug = MalSymbol("DEBUG-EVAL")
    if debug in repl_env and repl_env[debug] not in (MalFalse(), MalNil()):
        print(printer.pr_str(ast))
    if isinstance(ast, MalSymbol):
        if ast in repl_env:
            return repl_env[ast]
        else:
            raise MalNotFound
    elif isinstance(ast, MalList) and len(ast) > 0:
        func = EVAL(ast[0], repl_env)
        out = func(*[EVAL(item, repl_env) for item in ast[1:]])
        return out
    elif isinstance(ast, MalVector) and len(ast) > 0:
        return MalVector([EVAL(item, repl_env) for item in ast])
    elif isinstance(ast, MalHashMap) and len(ast) > 0:
        return MalHashMap({key: EVAL(ast[key], repl_env) for key in ast.keys()})
    else:
        return ast


def PRINT(mals: MalType) -> str:
    return printer.pr_str(mals)


def rep(string):
    ast = READ(string)
    mals = EVAL(ast, repl_env)
    string = PRINT(mals)
    return string


if __name__ == "__main__":
    while True:
        try:
            inp = m_input("user> ")
        except EOFError:
            break
        try:
            output = rep(inp)
            print(output)
        except MalEOFError:
            print("reached EOF while parsing")
        except MalNotFound:
            print("value not found")
        except MalEmptyExpr:
            pass
