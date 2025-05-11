from typing import Callable, List
from errors import m_EOFError, m_KeyError
from m_types import Boolean, Fn, Form, List_, Map, Nil, Symbol, Vector
from env import Env
from m_readline import input_
from reader import read_str
from core import ns
import sys

repl_env = Env(
    None,
)
for key in ns:
    repl_env[Symbol(key)] = ns[key]

repl_env[Symbol("eval")] = lambda a: eval_(a, repl_env)


def read(text: str) -> Form | None:
    ast = read_str(text)
    return ast


def eval_(ast: Form, env: Env) -> Form | Callable:
    while True:
        debug_eval = Symbol("DEBUG-EVAL")
        if (
            debug_eval in env
            and (flag := env[debug_eval]) is not Nil.NIL
            and flag is not Boolean.FALSE
        ):
            print("EVAL: " + str(ast))
        match ast:
            case Symbol():
                if ast in env:
                    return env[ast]  # type: ignore -- remove in step 5
                else:
                    raise m_KeyError(f"key {ast} not found")
            case List_():
                if len(ast) == 0:
                    return ast
                match ast:
                    case List_([Symbol("def!"), key, val]):
                        env[key] = eval_(val, env)
                        return env[key]  # type: ignore -- remove in step 5

                    case List_([Symbol("let*"), List_() | Vector() as binds, expr]):
                        key: Form | None = None
                        env = Env(env)
                        for x in binds:
                            if key:
                                env[key] = eval_(x, env)
                                key = None
                            else:
                                key = x
                        if key:
                            raise Exception("uneven binds in let*")
                        ast = expr
                        continue

                    case List_([Symbol("do"), *operand]):
                        for expr in operand[:-1]:
                            eval_(expr, env)
                        ast = operand[-1]
                        continue

                    case List_([Symbol("if"), condition, yes]):
                        if (
                            cond := eval_(condition, env)
                        ) is not Nil.NIL and cond is not Boolean.FALSE:
                            ast = yes
                        else:
                            ast = Nil.NIL

                    case List_([Symbol("if"), condition, yes, no]):
                        if (
                            cond := eval_(condition, env)
                        ) is not Nil.NIL and cond is not Boolean.FALSE:
                            ast = yes
                        else:
                            ast = no

                    case List_([Symbol("fn*"), List_() | Vector() as binds, impl]):

                        def closure(*exprs):
                            c_env = Env(env, binds, exprs)
                            return eval_(impl, c_env)

                        return Fn(impl, binds, env, closure)

                    case List_([callable, *rest]):
                        # if isinstance((fn := eval_(ast[0], env)), Callable):
                        #     return fn(*[eval_(i, env) for i in ast[1:]])
                        # else:
                        #     raise Exception(f"{str(fn)} is not callable")
                        f = eval_(callable, env)
                        if isinstance(f, Callable):
                            args = [eval_(arg, env) for arg in rest]
                            if isinstance(f, Fn):
                                env = Env(f.env, f.params, args)
                                ast = f.impl
                                continue
                            return f(*args)
                        else:
                            raise Exception(f"callable {callable} is no Callable")
                    case _:
                        raise Exception(f"ast {ast} did no match a list pattern")

            case Vector():
                return Vector([eval_(x, env) for x in ast])  # type: ignore
            case Map():
                map: List[Form] = []
                for x in ast:
                    map.append(x)
                    map.append(eval_(ast[x], env))  # type: ignore
                return Map().from_list(map)

            case _:
                return ast


def print_(exp: Form) -> str:
    text = str(exp)
    return text


def rep(text: str) -> str | None:
    ast = read(text)
    if ast is None:
        return None
    exp = eval_(ast, repl_env)
    text = print_(exp)  # type: ignore
    return text


rep("(def! not (fn* (a) (if a false true)))")
rep('(def! load-file (fn* (f) (eval (read-string (str "(do " (slurp f)"\nnil)")))))')


def main():
    while True:
        try:
            print(rep(input_("user> ")))
        except EOFError:
            print()
            break
        except m_EOFError as e:
            print("EOF", e.args)
        except m_KeyError as e:
            print("Key Error", e.args)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        rep(f"(def! *ARGV* ({' '.join([f'"{x}"' for x in sys.argv[2:]])}))")
        rep(f'(load-file "{sys.argv[1]}")')
    else:
        rep("(def! *ARGV* ())")
        main()
