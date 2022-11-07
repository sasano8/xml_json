from decimal import Decimal
from fractions import Fraction


def unsupported(x):
    raise NotImplementedError()


def value_to_token(x):
    return value_to_sql(x.value)


def value_to_sql(x):
    if isinstance(x, str):
        return "'" + x.replace("'", "\\'") + "'"
    elif isinstance(x, bool):
        return "true" if x else "false"
    elif isinstance(x, (int, float)):
        return str(x)
    elif x is None:
        return "null"
    elif isinstance(x, (Fraction, Decimal)):
        return str(x.__float__())
    elif isinstance(x, list):
        return "ARRAY[" + ",".join(value_to_token(_) for _ in x) + "]"
    elif isinstance(x, dict):
        raise TypeError()


types = {
    "value": value_to_token,
    "identifier": value_to_token,
    "alias": value_to_token,
    "datetime": value_to_token,
    "select": value_to_token,
    "from": value_to_token,
    "join": value_to_token,
    "where": value_to_token,
    "orderby": value_to_token,
    "groupby": value_to_token,
    "having": value_to_token,
}


operators = {
    "+": value_to_token,
    "-": value_to_token,
    "*": value_to_token,
    "/": value_to_token,
    "%": value_to_token,
    "^": unsupported,  # 累乗
    "|/": unsupported,
    "||/": unsupported,
    "!": unsupported,
    "!!": unsupported,
    "@": unsupported,
    "==": value_to_token,
    "!=": value_to_token,
    "like": value_to_token,
    "in": value_to_token,
    ">": value_to_token,
    "<": value_to_token,
    ">=": value_to_token,
    "<=": value_to_token,
    "if": unsupported,
    "elif": unsupported,
    "else": unsupported,
    # ビット演算
    "&": unsupported,
    "|": unsupported,
    "#": unsupported,  # ビットごとのXOR 構文と衝突 mysqlでは^
    "~": unsupported,
    "<<": unsupported,
    ">>": unsupported,
}

identifiers = {
    # "table": value_to_token,  # to table identifier from str
    "abs": value_to_token,  # @演算子は構文上衝突が多いので関数とする
    "pow": value_to_token,
    "unnest": value_to_token,
    "pow": value_to_token,
    "pow": value_to_token,
}
