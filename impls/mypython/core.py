from m_types import Boolean, List_, Number, Nil, String
from reader import read_str

ns = {
    "+": lambda a, b: Number(a + b),
    "-": lambda a, b: Number(a - b),
    "*": lambda a, b: Number(a * b),
    "/": lambda a, b: Number(a / b),
    "pr-str": lambda *a: String(" ".join([str(x) for x in a])),
    "str": lambda *a: String("".join([x.__str__(readably=False) for x in a])),
    "prn": lambda *a: print(" ".join(str(x) for x in a)) or Nil.NIL,
    "println": lambda *a: print(" ".join([x.__str__(readably=False) for x in a]))
    or Nil.NIL,
    "list": lambda *a: List_(a),
    "list?": lambda a: Boolean.TRUE if isinstance(a, List_) else Boolean.FALSE,
    "empty?": lambda a: Boolean.TRUE if (len(a) == 0) else Boolean.FALSE,
    "count": lambda a: Number(len(a)),
    "=": lambda a, b: Boolean.TRUE if a == b else Boolean.FALSE,
    "<": lambda a, b: Boolean.TRUE if a < b else Boolean.FALSE,
    "<=": lambda a, b: Boolean.TRUE if a <= b else Boolean.FALSE,
    ">": lambda a, b: Boolean.TRUE if a > b else Boolean.FALSE,
    ">=": lambda a, b: Boolean.TRUE if a >= b else Boolean.FALSE,
    "read-string": lambda a: read_str(a),
    "slurp": lambda a: String(open(a).read()),
}
