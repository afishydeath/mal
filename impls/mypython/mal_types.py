class MalType:
    pass

class MalList(MalType):
    def __init__(self, contents:list[MalType]) -> None:
        super().__init__()
        self.contents = contents

    def __iter__(self):
        self.pos = 0
        return self

    def __next__(self):
        if self.pos == len(self.contents):
            raise StopIteration
        self.pos+=1
        return self.contents[self.pos-1]

    def append(self, item:MalType) -> None:
        self.contents.append(item)


class MalInteger(MalType):
    def __init__(self, value:int) -> None:
        super().__init__()
        self.value = value

    def __str__(self) -> str:
        return self.value.__str__()

class MalSymbol(MalType):
    def __init__(self, symbol:str) -> None:
        super().__init__()
        self.symbol = symbol

    def __str__(self) -> str:
        return self.symbol
