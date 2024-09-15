from mal_types import MalType, MalList

def pr_str(mals:MalType) -> str:
    if isinstance(mals, MalList):
        out = []
        for mal in mals:
            out.append(pr_str(mal))
        return '('+' '.join(out)+')'
    else:
        return str(mals)
