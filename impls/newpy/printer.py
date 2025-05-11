from types_ import MalType, MalList, MalNumber, MalSymbol


def pr_str(mal: MalType) -> str:
    match mal:
        case MalList():
            return "(" + " ".join([pr_str(x) for x in mal.value]) + ")"
        case MalNumber():
            return str(mal.value)
        case MalSymbol():
            return mal.value
        case _:
            raise Exception(f"pr_str called on unimplemented type for value {mal}")
