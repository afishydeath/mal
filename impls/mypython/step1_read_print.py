from m_readline import input_


def read(text):
    return text


def eval_(ast, env):
    return ast


def print_(exp):
    return exp


def rep(text):
    return print_(eval_(read(text), ""))


def main():
    while True:
        try:
            print(rep(input_("user> ")))
        except EOFError:
            break


if __name__ == "__main__":
    main()
