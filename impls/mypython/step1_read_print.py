#!/usr/bin/env nix-shell
#! nix-shell -i python3 --packages python312 python312Packages.regex
import reader, printer, mal_readline
from mal_types import MalType

def READ(string:str) -> MalType:
    return reader.read_str(string)

def EVAL(mals:MalType) -> MalType:
    return mals

def PRINT(mals:MalType) -> str:
    return printer.pr_str(mals)

def rep(string:str) -> str:
    mals = READ(string)
    mals = EVAL(mals)
    return PRINT(mals)

def main() -> None:
    while True:
        try:
            print(rep(mal_readline.input_("user> ")))
        except EOFError:
            return None

if __name__ == "__main__":
    main()
