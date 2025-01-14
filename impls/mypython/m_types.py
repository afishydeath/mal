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


class MalFunctionObject:
    def __init__(self, ast: "MalType", params: MalList, env: "Env", fn: MalFunction):
        self.ast = ast
        self.params = params
        self.env = env
        self.fn = fn


class MalNil:
    def __len__(self):
        return 0

    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, MalNil):
            return True
        return False


class MalTrue:
    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, MalTrue):
            return True
        return False


class MalFalse:
    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, MalFalse):
            return True
        return False


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
