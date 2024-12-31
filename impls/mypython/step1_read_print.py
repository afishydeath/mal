from m_readline import m_input 
from m_types import MalType
import reader
import printer

def READ(string : str) -> MalType:
    return reader.read_str(string)

def EVAL(mals : MalType) -> MalType:
    return mals

def PRINT(mals : MalType) -> str:
    return printer.pr_str(mals)

def rep(string):
    mals = READ(string)
    print(mals)
    mals = EVAL(mals)
    string = PRINT(mals)
    return string
if __name__ == "__main__":
    while True:
        try:
            inp = m_input("user> ")
        except EOFError:
            break
        print(rep(inp))
