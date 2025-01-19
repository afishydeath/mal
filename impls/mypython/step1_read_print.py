from errors import m_EOFError
from m_types import Form
from m_readline import input_
from reader import read_str


def read(text: str) -> Form | None:
    ast = read_str(text)
    return ast


def eval_(ast: Form, env) -> Form:
    return ast


def print_(exp: Form) -> str:
    text = exp.__str__()
    return text


def rep(text: str) -> str | None:
    ast = read(text)
    if ast is None:
        return None
    exp = eval_(ast, "")
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


if __name__ == "__main__":
    main()
