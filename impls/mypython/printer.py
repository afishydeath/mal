from m_types import MalType, MalList

def pr_str(mals : MalType) -> str:
    if isinstance(mals,MalList):
        stringlist = []
        for mal in mals:
            stringlist.append(pr_str(mal))
        return '('+(' '.join(stringlist))+')'
    else:
        return str(mals)
