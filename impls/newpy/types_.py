class MalType:
    pass


class MalList(MalType):
    def __init__(self, value: list[MalType]):
        self.value: list[MalType] = value

    def append(self, item: MalType):
        self.value.append(item)


class MalNumber(MalType):
    def __init__(self, value: int):
        self.value = value


class MalSymbol(MalType):
    def __init__(self, value: str):
        self.value = value
