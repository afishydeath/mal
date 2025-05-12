from types_ import (
    MalFn,
    MalKeyword,
    MalList,
    MalMap,
    MalNil,
    MalString,
    MalSymbol,
    MalType,
    MalVector,
)
from env import Env
from readline_ import input_
import reader
import printer
import logging

logging.basicConfig(filename="step.log", level=logging.INFO, filemode="w")
logger = logging.getLogger(__name__)

tmp = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a // b,
}

repl_env = Env(MalNil())
for k in tmp:
    repl_env.set(MalSymbol(k), MalFn(tmp[k]))


def READ(string: str) -> MalType:
    ast = reader.read_str(string)
    logger.info(repr(ast))
    return ast


def EVAL(ast: MalType, env) -> MalType:
    if MalSymbol("DEBUG-EVAL") in env and env.get(MalSymbol("DEBUG-EVAL")):
        print(f"EVAL: {printer.pr_str(ast, readably=True)}")
    match ast:
        case MalSymbol():
            if ast in env:
                return env.get(ast)
            else:
                raise KeyError(f"{ast} not found in {env}")

        case MalList([]):
            return ast

        case MalList([MalSymbol("def!"), key, value]):
            env.set(key, tmp := EVAL(value, env))
            return tmp

        case MalList([MalSymbol("let*"), MalList() | MalVector() as bindings, body]):
            new_env = Env(env)
            key_flag = True
            key: MalType = MalNil()
            for item in bindings:
                if key_flag:
                    key = item
                    key_flag = False
                else:
                    if isinstance(key, MalSymbol):
                        new_env.set(key, EVAL(item, new_env))
                        key_flag = True
                    else:
                        raise KeyError(f"key {key} is not a symbol")
            if not key_flag:
                raise KeyError(f"Uneven key value pairs for definitions {bindings}")
            return EVAL(body, new_env)

        case MalList([first, *rest]):
            f = EVAL(first, env)
            if not isinstance(f, MalFn):
                raise KeyError(f"Value {f} is not callable")
            return f(*[EVAL(x, env) for x in rest])

        case MalVector():
            return MalVector([EVAL(x, env) for x in ast])

        case MalMap():
            tmp_map = MalMap({key: EVAL(ast[key], env) for key in ast})
            return tmp_map

        case _:
            return ast


def PRINT(exp: MalType) -> str:
    string = printer.pr_str(exp, readably=True)
    logger.info(string)
    return string


def rep(string):
    return PRINT(EVAL(READ(string), repl_env))


if __name__ == "__main__":
    while True:
        try:
            print(rep(input_("user> ")))
        except EOFError:
            print()
            break
        except Exception as e:
            print(e)
