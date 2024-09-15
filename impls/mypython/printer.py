from mal_types import MalType, List

def pr_str(ast:MalType) -> str:
    if isinstance(ast, List):
        out = []
        for mal in ast:
            out.append(pr_str(mal))
        return '('+' '.join(out)+')'
    else:
        return str(ast)
