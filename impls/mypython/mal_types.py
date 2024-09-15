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

    def __str__(self):
        return str(self.contents)

    def __repr__(self):
        return f"MalList({repr(self.contents)})"

    def __len__(self):
        return len(self.contents)

    def __getitem__(self, pos):
        return self.contents[pos]

    def append(self, item:MalType) -> None:
        self.contents.append(item)


class MalInteger(MalType):
    def __init__(self, value:int) -> None:
        super().__init__()
        self.value = value

    def __str__(self) -> str:
        return self.value.__str__()

    def __repr__(self) -> str:
        return f"MalInteger({self.value})"

    def __add__(self, other):
        if isinstance(other,MalInteger):
            return MalInteger(self.value+other.value)
        raise TypeError(f"Unsupported addition between {type(self)} and {type(other)}")

    def __sub__(self, other):
        if isinstance(other,MalInteger):
            return MalInteger(self.value-other.value)
        raise TypeError(f"Unsupported addition between {type(self)} and {type(other)}")

    def __mul__(self, other):
        if isinstance(other,MalInteger):
            return MalInteger(self.value*other.value)
        raise TypeError(f"Unsupported addition between {type(self)} and {type(other)}")

    def __floordiv__(self, other):
        if isinstance(other,MalInteger):
            return MalInteger(self.value//other.value)
        raise TypeError(f"Unsupported addition between {type(self)} and {type(other)}")

        

class MalSymbol(MalType):
    def __init__(self, symbol:str) -> None:
        super().__init__()
        self.symbol = symbol

    def __str__(self) -> str:
        return self.symbol

    def __repr__(self):
        return f"MalSymbol({self.symbol})"
