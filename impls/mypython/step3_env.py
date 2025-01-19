from typing import Callable, List
from errors import m_EOFError, m_KeyError
from m_types import Boolean, Form, List_, Map, Nil, Number, Symbol, Vector
from env import Env
from m_readline import input_
from reader import read_str

repl_env = Env(
    None,
    contents={
        Symbol("+"): lambda a, b: Number(a + b),
        Symbol("-"): lambda a, b: Number(a - b),
        Symbol("*"): lambda a, b: Number(a * b),
        Symbol("/"): lambda a, b: Number(a / b),
    },
)


def read(text: str) -> Form | None:
    ast = read_str(text)
    return ast


def eval_(ast: Form, env: Env) -> Form:
    debug_eval = Symbol("DEBUG-EVAL")
    # if (flag := env.get_(debug_eval)) and (
    #     flag is not Nil.NIL and flag is not Boolean.FALSE
    # ):
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
                    return eval_(expr, env)
                case _:
                    if isinstance((fn := eval_(ast[0], env)), Callable):
                        return fn(*[eval_(i, env) for i in ast[1:]])
                    else:
                        raise Exception(f"{str(fn)} is not callable")

        case Vector():
            return Vector([eval_(x, env) for x in ast])
        case Map():
            map: List[Form] = []
            for x in ast:
                map.append(x)
                map.append(eval_(ast[x], env))
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
    text = print_(exp)
    return text


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
    main()
