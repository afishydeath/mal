from m_types import (
    MalFalse,
    MalFunction,
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
    elif isinstance(mals, MalFunction):
        return "#<function>"
    elif isinstance(mals, MalString):
        if print_readably:
            formatted = (
                str(mals)
                .replace("\n", ";n")
                .replace('"', ';"')
                .replace("\\", ";;")
                .replace(";", "\\")
            )
            return f'"{formatted}"'
        else:
            return '"' + str(mals) + '"'

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
        raise Exception(f"printing of mal {type(mals)} type not implemented")
