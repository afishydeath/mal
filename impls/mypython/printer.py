from m_types import MalBoolean, MalHashMap, MalKeyword, MalList, MalNil, MalNumber, MalString, MalSymbol, MalType, MalVector

def pr_str(mals : MalType) -> str:
    if isinstance(mals, MalNumber):
        return str(mals)
    elif isinstance (mals, MalBoolean):
        return str(mals).lower()
    elif isinstance(mals, MalNil):
        return 'nil'
    elif isinstance(mals, MalKeyword):
        return ':'+str(mals)
    elif isinstance(mals, MalSymbol):
        return str(mals)
    elif isinstance(mals, MalString):
        return '"'+str(mals)+'"'
    elif isinstance(mals, MalList):
        return '(' + ' '.join([pr_str(mal) for mal in mals]) + ')'
    elif isinstance(mals, MalVector):
        return '[' + ' '.join([pr_str(mal) for mal in mals]) + ']'
    elif isinstance(mals, MalHashMap):
        return '{' + ' '.join([pr_str(key)+' '+pr_str(mals[key]) for key in mals.keys()]) + '}'
    else:
        raise Exception("printing of mal type not implemented")
