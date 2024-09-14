def pr_str(mals):
    if isinstance(mals, list):
        out = []
        for mal in mals:
            out.append(pr_str(mal))
        return '('+' '.join(out)+')'
    else:
        return str(mals)

if __name__ == "__main__":
    print(pr_str(['+', 1, ['+', 2, 3]]))
