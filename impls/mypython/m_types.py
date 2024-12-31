class MalList(list["MalType"]):
    pass

class MalNumber(int):
    pass

class MalSymbol(str):
    pass

MalType = (MalList | MalNumber | MalSymbol)
