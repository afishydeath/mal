class MalList(list["MalType"]):
    list_type : str = "("
    def make_vector(self):
        self.list_type = '['

class MalNumber(int):
    pass

class MalSymbol(str):
    pass

MalEmptyReturn = None


MalNil = None

MalBoolean = bool

MalListOrEmpty = (MalList | MalEmptyReturn)

MalType = (MalList | MalNumber | MalSymbol | MalNil | MalBoolean | MalEmptyReturn)
