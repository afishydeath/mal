class MalSequential(list["MalType"]):
    pass

class MalList(MalSequential):
    pass

class MalVector(MalSequential):
    pass

class MalHashMap(dict["MalType", "MalType"]):
    pass

class MalNumber(int):
    pass

class MalSymbol(str):
    pass

class MalKeyword(str):
    pass

class MalString(str):
    pass

class MalEOFError(Exception):
    pass

class MalEmptyExpr(Exception):
    pass

class MalNotFound(Exception):
    pass

class MalNil():
    pass

MalEmptyReturn = None



MalBoolean = bool

MalType = (MalSequential | MalNumber | MalSymbol | MalNil | MalBoolean | MalEmptyReturn | MalString | MalKeyword | MalHashMap)
