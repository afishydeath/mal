from types_ import (
    MalFn,
    MalList,
    MalMap,
    MalNil,
    MalString,
    MalSymbol,
    MalType,
    MalVector,
    MalFnTCO,
)
from env import Env
from readline_ import input_
import core
import reader
import printer
import logging
import sys

logging.basicConfig(filename="step.log", level=logging.INFO, filemode="w")
logger = logging.getLogger(__name__)

_binds = MalList[MalSymbol]([MalSymbol(x) for x in core.ns.keys()])
_exprs = MalList([MalFn(x) for x in core.ns.values()])
repl_env = Env(MalNil(), _binds, _exprs)


def quasiquote(ast: MalType, vec_flag=False) -> MalType:
    match ast:
        case MalList([MalSymbol("unquote"), second]) if not vec_flag:
            return second

        case MalList():
            result = MalList()
            for elt in ast.value[::-1]:
                match elt:
                    case MalList([MalSymbol("splice-unquote"), second]):
                        result = MalList([MalSymbol("concat"), second, result])

                    case _:
                        result = MalList([MalSymbol("cons"), quasiquote(elt), result])
            return result

        case MalVector():
            return MalList(
                [MalSymbol("vec"), quasiquote(MalList(ast.value), vec_flag=True)]
            )

        case MalMap() | MalSymbol():
            return MalList([MalSymbol("quote"), ast])

        case _:
            return ast


def READ(string: str) -> MalType:
    ast = reader.read_str(string)
    # logger.info(repr(ast))
    return ast


def EVAL(ast: MalType, env) -> MalType:
    while True:
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
            case MalList([MalSymbol("defmacro!"), key, value]):
                f = EVAL(value, env)
                if not isinstance(f, MalFnTCO):
                    raise TypeError(f"evaluated value {f} is not a MalFnTco")
                f.is_macro = True
                env.set(key, f)
                return f

            case MalList(
                [MalSymbol("let*"), MalList() | MalVector() as bindexpr, body]
            ):
                _env = Env(env, MalList(), MalList())
                key_flag = True
                key: MalSymbol
                for item in bindexpr:
                    if key_flag:
                        key = item
                        key_flag = False
                    else:
                        _env.set(key, EVAL(item, _env))
                        key_flag = True
                env = _env
                ast = body

            case MalList([MalSymbol("do"), *rest, last]):
                for item in rest:
                    EVAL(item, env)
                ast = last

            case MalList([MalSymbol("if"), condition, then]):
                if EVAL(condition, env):
                    ast = then
                else:
                    ast = MalNil()

            case MalList([MalSymbol("if"), condition, then, otherwise]):
                if EVAL(condition, env):
                    ast = then
                else:
                    ast = otherwise

            case MalList([MalSymbol("fn*"), binds, do]):

                def closure(*exprs: MalType) -> MalType:
                    return EVAL(do, Env(env, binds, MalList(exprs)))

                return MalFnTCO(ast=do, params=binds, env=env, fn=MalFn(closure))

            case MalList([MalSymbol("quote"), arg]):
                return arg

            case MalList([MalSymbol("quasiquote"), arg]):
                ast = quasiquote(arg)

            case MalList([first, *rest]):
                f = EVAL(first, env)
                rest = [EVAL(x, env) for x in rest]
                match f:
                    case MalFn():
                        return f(*rest)
                    case MalFnTCO():
                        if f.is_macro:
                            ast = f.fn(*rest)
                        else:
                            ast = f.ast
                            env = Env(f.env, f.params, MalList(rest))
                            logger.info(ast)
                            logger.info(env)
                    case _:
                        raise KeyError(f"Value {f} is not callable")

            case MalVector():
                return MalVector([EVAL(x, env) for x in ast])

            case MalMap():
                tmp_map = MalMap({key: EVAL(ast[key], env) for key in ast.value.keys()})
                return tmp_map

            case _:
                return ast


def PRINT(exp: MalType) -> str:
    string = printer.pr_str(exp, readably=True)
    # logger.info(string)
    return string


def rep(string):
    return PRINT(EVAL(READ(string), repl_env))


def eval_(a: MalType) -> MalType:
    return EVAL(a, repl_env)


repl_env.set(MalSymbol("eval"), MalFn(eval_))
repl_env.set(MalSymbol("*ARGV*"), MalList())
rep("(def! not (fn* (a) (if a false true)))")
rep('(def! load-file (fn* (f) (eval (read-string (str "(do " (slurp f) "\nnil)")))))')
rep(
    "(defmacro! cond (fn* (& xs) (if (> (count xs) 0) (list 'if (first xs) (if (> (count xs) 1) (nth xs 1) (throw \"odd number of forms to cond\")) (cons 'cond (rest (rest xs)))))))"
)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        logger.info(sys.argv)
        repl_env.set(MalSymbol("*ARGV*"), MalList([MalString(x) for x in sys.argv[2:]]))
        rep(f'(load-file "{sys.argv[1]}")')
    else:
        while True:
            try:
                print(rep(input_("user> ")))
            except EOFError:
                print()
                break
            except Exception as e:
                print(e)
