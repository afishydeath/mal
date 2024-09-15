class Number(int):
    def __str__(self) -> str:
        return super().__str__()

class Symbol(str):
    def __str__(self) -> str:
        return self

class List(tuple['MalType', ...]):
    def __str__(self) -> str:
        return '(' + super().__str__() + ')'

MalType = (Number | Symbol | List)
