from pydantic import BaseModel, Field
from typing import List, Dict, Tuple, Union


class Ident:
    ...


class Func:
    name: str

    def evalute(self):
        ...


class From(BaseModel):
    name: str = Field("from", const=True)
    # nodes: Tuple[]


class Join(BaseModel):
    name: str = Field("from", const=True)
    nodes: Tuple[From, "Join"]


class Where(BaseModel):
    name: str = Field("from", const=True)
    nodes: Tuple[Union[From, Join]]


class GroupBy(BaseModel):
    name: str = Field("from", const=True)
    nodes: Tuple[Union[From, Join, Where]]


class Having(BaseModel):
    name: str = Field("from", const=True)
    nodes: Tuple[GroupBy]


class OrderBy(BaseModel):
    name: str = Field("from", const=True)
    nodes: Tuple[Union[From, Join, Where, GroupBy]]


class Select(BaseModel):
    name: str = Field("from", const=True)
    nodes: Tuple[Union[From, Join, Where, GroupBy, OrderBy]]


class Schema(BaseModel):
    version: str = Field("0.1", const=True)
    name: str
    ignore_attrs: bool = True
    ignore_help: bool = True
    allow_alias: bool = True
    allow_param: bool = True
    case_sensitive: bool = True
    nodes: Dict = {
        "from": From,
        "join": Join,
        "where": Where,
        "groupby": GroupBy,
        "having": Having,
        "orderby": OrderBy,
        "select": Select,
    }
    types: Dict = {
        "null": None,
        "str": str,
        "int": int,
        "float": float,
        "bool": bool,
        "list": list,
        "dict": dict,
        "ident": Ident,
    }
    bin_operators: Dict = {
        "+": None,
        "-": None,
        "*": None,
        "/": None,
        "==": None,
        "!=": None,
        ">": None,
        "<": None,
        "<=": None,
        ">=": None,
        "and": None,
        "or": None,
        "not": None,
        "xor": None,
    }
    allow_unkown_identifiers: bool = True
    identifiers: Dict = {}
    allow_unkown_functions: bool = True
    functions: Dict = {
        "int": int,
        "str": str,
        "float": float,
        "bool": bool,
        "list": list,
        "dict": dict,
    }

    # startswith: 前方一致
    # endswith: 後方一致

    def export_document(self):
        ...


class Parser(BaseModel):
    ebnf: str
    spec: Schema

    def parse(self, *args, **kwargs):
        ...

    def evalute(self, *args, **kwargs):
        tree = self.parse(*args, **kwargs)
        return tree.evalute()


class Parser2:
    def __init_subclass__(cls, schema: Schema):
        schema.case_sensitive


class Evaluator:
    ...


def from_protobuf(message):
    # https://qiita.com/yukina-ge/items/98fe190cef2024d45fbd
    if message.type == "double":
        ...
    elif message.type == "float":
        ...
    elif message.type == "int32":
        ...
    elif message.type == "int64":
        ...
    elif message.type == "uint32":
        ...
    elif message.type == "uint64":
        ...
    elif message.type == "sint32":
        ...
    elif message.type == "sint64":
        ...
    elif message.type == "fixed32":
        ...
    elif message.type == "fixed64":
        ...
    elif message.type == "sfixed32":
        ...
    elif message.type == "sfixed64":
        ...
    elif message.type == "bool":
        ...
    elif message.type == "string":
        ...
    elif message.type == "bytes":
        ...
    else:
        raise Exception()
