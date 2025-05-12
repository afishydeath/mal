from types_ import (
    MalFn,
    MalList,
    MalMap,
    MalNil,
    MalSymbol,
    MalType,
    MalVector,
)
from env import Env
from readline_ import input_
import core
import reader
import printer
import logging

logging.basicConfig(filename="step.log", level=logging.INFO, filemode="w")
logger = logging.getLogger(__name__)

_binds = MalList[MalSymbol]([MalSymbol(x) for x in core.ns.keys()])
_exprs = MalList([MalFn(x) for x in core.ns.values()])
repl_env = Env(MalNil(), _binds, _exprs)


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

        case MalList([MalSymbol("let*"), MalList() | MalVector() as bindexpr, body]):
            binds: MalList[MalSymbol] = MalList[MalSymbol]()
            exprs: MalList = MalList()
            key_flag = True
            for item in bindexpr:
                if key_flag:
                    binds.append(item)
                    key_flag = False
                else:
                    exprs.append(item)
                    key_flag = True
            new_env = Env(env, binds, exprs)
            return EVAL(body, new_env)

        case MalList([MalSymbol("do"), *rest]):
            last: MalType = MalNil()
            for item in rest:
                last = EVAL(item, env)
            return last

        case MalList([MalSymbol("if"), condition, then]):
            if EVAL(condition, env):
                return EVAL(then, env)
            else:
                return MalNil()

        case MalList([MalSymbol("if"), condition, then, otherwise]):
            if EVAL(condition, env):
                return EVAL(then, env)
            else:
                return EVAL(otherwise, env)

        case MalList([MalSymbol("fn*"), binds, do]):

            def closure(*exprs: MalType):
                return EVAL(do, Env(env, binds, MalList(exprs)))

            return MalFn(closure)

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
