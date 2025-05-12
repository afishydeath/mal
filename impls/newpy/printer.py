from types_ import MalType


def pr_str(mal: MalType, readably=False) -> str:
    return mal.__str__(readably=readably)
