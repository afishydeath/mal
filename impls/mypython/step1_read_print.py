#!/usr/bin/env nix-shell
#! nix-shell -i python3 --packages python312 python312Packages.regex
import reader, printer, mal_readline

def READ(string):
    return reader.read_str(string)

def EVAL(mals):
    return mals

def PRINT(mals):
    return printer.pr_str(mals)

def rep(string):
    mals = READ(string)
    mals = EVAL(mals)
    return PRINT(mals)

def main():
    while True:
        try:
            print(rep(mal_readline.input_("user> ")))
        except EOFError:
            return 0

if __name__ == "__main__":
    main()
