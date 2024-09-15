#!/usr/bin/env nix-shell
#! nix-shell -i python3 --packages python312 python312Packages.regex
import reader, printer, mal_readline
from mal_types import MalType, Symbol, List

repl_env = {
        '+' : lambda a,b:a+b,
        '-' : lambda a,b:a-b,
        '*' : lambda a,b:a*b,
        '/' : lambda a,b:a//b,
        }

def READ(string:str) -> MalType:
    return reader.read_str(string)

def EVAL(ast:MalType, repl_env:dict):
    # print(ast)
    if isinstance(ast, Symbol):
        return repl_env[str(ast)]
    elif isinstance(ast, List) and len(ast) > 0:
        function = EVAL(ast[0], repl_env)
        rest = [EVAL(x,repl_env) for x in ast[1:]]
        # print(rest)
        return function(*rest)
    return ast

def PRINT(ast:MalType) -> str:
    return printer.pr_str(ast)

def rep(string:str) -> str:
    ast = READ(string)
    ast = EVAL(ast, repl_env)
    return PRINT(ast)

def main() -> None:
    while True:
        try:
            print(rep(mal_readline.input_("user> ")))
        except EOFError:
            return None
        except KeyError:
            print("Error: KeyError")

if __name__ == "__main__":
    main()
