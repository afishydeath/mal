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


class MalArgumentsWrong(Exception):
    pass


class MalFunction:
    def __init__(self, function):
        self.function = function

    def __call__(self, *args: "MalType") -> "MalType":
        return self.function(*args)


class MalNil:
    pass


class MalTrue:
    pass


class MalFalse:
    pass


MalEmptyReturn = None


MalBoolean = MalTrue | MalFalse

MalType = (
    MalSequential
    | MalNumber
    | MalSymbol
    | MalNil
    | MalBoolean
    | MalEmptyReturn
    | MalString
    | MalKeyword
    | MalHashMap
    | MalFunction
)
