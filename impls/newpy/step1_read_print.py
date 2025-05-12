from types_ import MalType
from readline_ import input_
import reader
import printer
import logging

logging.basicConfig(filename="step1.log", level=logging.INFO, filemode="w")
logger = logging.getLogger(__name__)


def READ(string: str) -> MalType:
    ast = reader.read_str(string)
    logger.info(repr(ast))
    return ast


def EVAL(ast: MalType, env) -> MalType:
    return ast


def PRINT(exp: MalType) -> str:
    string = printer.pr_str(exp, readably=True)
    logger.info(string)
    return string


def rep(string):
    return PRINT(EVAL(READ(string), ""))


if __name__ == "__main__":
    while True:
        try:
            print(rep(input_("user> ")))
        except EOFError:
            print()
            break
        except Exception as e:
            print(e)
