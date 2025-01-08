from Env import Env
from m_readline import m_input
from m_types import (
    MalArgumentsWrong,
    MalEOFError,
    MalEmptyExpr,
    MalFalse,
    MalFunction,
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

repl_env: Env = Env(MalNil())
repl_env.set(MalSymbol("+"), MalFunction(lambda a, b: MalNumber(a + b)))
repl_env.set(MalSymbol("-"), MalFunction(lambda a, b: MalNumber(a - b)))
repl_env.set(MalSymbol("*"), MalFunction(lambda a, b: MalNumber(a * b)))
repl_env.set(MalSymbol("/"), MalFunction(lambda a, b: MalNumber(a / b)))
# repl_env.set(MalSymbol('DEBUG-EVAL'), MalBoolean(True))


def READ(string: str) -> MalType:
    return reader.read_str(string)


def EVAL(ast: MalType, env):
    debug = MalSymbol("DEBUG-EVAL")
    try:
        result = env.get(debug)
        if result not in (MalFalse(), MalNil()):
            print("EVAL: " + printer.pr_str(ast, print_readably=True))
    except MalNotFound:
        pass

    if isinstance(ast, MalSymbol):
        return env.get(ast)
    elif isinstance(ast, MalList) and len(ast) > 0:
        match ast[0]:
            case MalSymbol("def!"):
                env.set(ast[1], EVAL(ast[2], env))
                return env.get(ast[1])
            case MalSymbol("let*"):
                new_env = Env(env)
                if isinstance(ast[1], MalList):
                    definitions: MalList = ast[1]
                    for i in range(0, len(definitions), 2):
                        new_env.set(definitions[i], EVAL(definitions[i + 1], new_env))
                    return EVAL(ast[2], new_env)
            case _:
                func = EVAL(ast[0], env)
                out = func(*[EVAL(item, env) for item in ast[1:]])
                return out
    elif isinstance(ast, MalVector) and len(ast) > 0:
        return MalVector([EVAL(item, env) for item in ast])
    elif isinstance(ast, MalHashMap) and len(ast) > 0:
        return MalHashMap({key: EVAL(ast[key], env) for key in ast.keys()})
    else:
        return ast


def PRINT(mals: MalType) -> str:
    return printer.pr_str(mals, print_readably=True)


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
        except MalNotFound as e:
            print(e.args[0])
        except MalEmptyExpr:
            pass
