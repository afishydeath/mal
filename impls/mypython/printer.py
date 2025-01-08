from m_types import (
    MalFalse,
    MalHashMap,
    MalKeyword,
    MalList,
    MalNil,
    MalNumber,
    MalString,
    MalSymbol,
    MalTrue,
    MalType,
    MalVector,
)


def pr_str(mals: MalType, print_readably=False) -> str:
    if isinstance(mals, MalNumber):
        return str(mals)
    elif isinstance(mals, MalTrue):
        return "true"
    elif isinstance(mals, MalFalse):
        return "false"
    elif isinstance(mals, MalNil):
        return "nil"
    elif isinstance(mals, MalKeyword):
        return ":" + str(mals)
    elif isinstance(mals, MalSymbol):
        return str(mals)
    elif isinstance(mals, MalString):
        if print_readably:
            return '"' + str(mals) + '"'
        else:
            formatted = ""
            escaped = False
            for i in range(len(mals)):
                if escaped:
                    escaped = False
                else:
                    if mals[i] != "\\":
                        formatted += mals[i]
                    else:
                        escaped = True
                        match mals[i + 1]:
                            case "n":
                                formatted += "\n"
                            case "\\":
                                formatted += "\\"
                            case '"':
                                formatted += '"'
                            case _:
                                raise Exception("escaped non-handled character")
            return formatted

    elif isinstance(mals, MalList):
        return "(" + " ".join([pr_str(mal) for mal in mals]) + ")"
    elif isinstance(mals, MalVector):
        return "[" + " ".join([pr_str(mal) for mal in mals]) + "]"
    elif isinstance(mals, MalHashMap):
        return (
            "{"
            + " ".join([pr_str(key) + " " + pr_str(mals[key]) for key in mals.keys()])
            + "}"
        )
    else:
        raise Exception("printing of mal type not implemented")
