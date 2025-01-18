import printer
import reader
from core import ns
from Env import Env
from m_readline import m_input
from m_types import (
    MalArgumentsWrong,
    MalEmptyExpr,
    MalEOFError,
    MalFalse,
    MalFunction,
    MalFunctionObject,
    MalHashMap,
    MalList,
    MalNil,
    MalNotFound,
    MalSymbol,
    MalType,
    MalVector,
)

repl_env: Env = Env(MalNil())
for key in ns.keys():
    repl_env.set(MalSymbol(key), ns[key])


def READ(string: str) -> MalType:
    return reader.read_str(string)


def EVAL(ast: MalType, env):
    while True:
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
                    env.set(ast[1], EVAL(ast[2], env))  # type: ignore
                    return env.get(ast[1])  # type: ignore
                case MalSymbol("let*"):
                    new_env = Env(env)
                    if isinstance(ast[1], MalList):
                        definitions: MalList = ast[1]  # type: ignore
                        for i in range(0, len(definitions), 2):
                            new_env.set(
                                definitions[i],  # type: ignore
                                EVAL(definitions[i + 1], new_env),  # type: ignore
                            )
                        env = new_env
                        ast = ast[2]
                    else:
                        raise MalArgumentsWrong
                case MalSymbol("do"):
                    for item in ast[1:-1]:
                        EVAL(item, env)
                    ast = ast[-1]
                case MalSymbol("if"):
                    condition = EVAL(ast[1], env)
                    if condition not in (MalFalse(), MalNil()):
                        ast = ast[2]
                    elif len(ast) == 4:
                        ast = ast[3]
                    else:
                        return MalNil()
                case MalSymbol("fn*"):

                    def closure(*args: MalType):
                        c_env = Env(env, binds=ast[1], exprs=args)  # type: ignore
                        return EVAL(ast[2], c_env)

                    fn = MalFunction(closure)

                    return MalFunctionObject(ast[2], ast[1], env, fn)  # type: ignore
                case _:
                    func = EVAL(ast[0], env)
                    args = [EVAL(item, env) for item in ast[1:]]
                    if isinstance(func, MalFunctionObject):
                        env = Env(func.env, func.params, MalList(args))
                        ast = func.fn
                        continue
                    out = func(*args)  # type: ignore
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
    string = PRINT(mals)  # type: ignore
    return string


rep("(def! not (fn* (a) (if a false true)))")

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
