from types_ import (
    MalFalse,
    MalFn,
    MalList,
    MalMap,
    MalNil,
    MalSymbol,
    MalType,
    MalVector,
)
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
repl_env = {MalSymbol(s): MalFn(tmp[s]) for s in tmp.keys()}


def READ(string: str) -> MalType:
    ast = reader.read_str(string)
    logger.info(repr(ast))
    return ast


def EVAL(ast: MalType, env) -> MalType:
    if "DEBUG-EVAL" in env and env["DEBUG-EVAL"] not in [MalNil(), MalFalse()]:
        print(f"Eval: {printer.pr_str(ast, readably=True)}")
    match ast:
        case MalSymbol():
            if ast in env:
                return env[ast]
            else:
                raise KeyError(f"Value {ast} not in env {env}")

        case MalList([]):
            return ast

        case MalList():
            f = EVAL(ast[0], env)
            if not isinstance(f, MalFn):
                raise KeyError(f"Value {f} is not callable")
            return f(*[EVAL(x, env) for x in ast[1:]])

        case MalVector():
            return MalVector([EVAL(x, env) for x in ast])

        case MalMap():
            tmp_map = MalMap()
            for key in ast:
                tmp_map[key] = EVAL(ast[key], env)
            logger.info(tmp_map)
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
