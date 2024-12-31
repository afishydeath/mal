from m_types import MalType, MalList

def pr_str(mals : MalType) -> str:
    if isinstance(mals,MalList):
        stringlist = []
        for mal in mals:
            stringlist.append(pr_str(mal))

        brackets = '()'
        if mals.list_type == '[':
            brackets = '[]'
        return brackets[0]+(' '.join(stringlist))+brackets[1]
    else:
        return str(mals)
