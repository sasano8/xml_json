import json
from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel, Extra, Field, conlist


def __repr__(self):
    meta = ""
    if self.attrs:
        meta += f" {json.dumps(self.attrs, ensure_ascii=False)}"

    if self.help:
        meta += f' "{self.help}"'

    if len(self.elements) < 2:
        it = " ".join(repr(x) for x in self.elements)
        return it
    else:
        it = " ".join(repr(x) + "\n" for x in self.elements)
        return it


def __iter__(self):
    return self.elements.__iter__()


def __str__(self):
    return self.__repr__()


class NodeAbc:
    ...


class NodeBase(BaseModel, NodeAbc, extra=Extra.forbid):
    __iter__ = __iter__
    __repr__ = __repr__
    __str__ = __str__

    def dict(self, *args, **kwargs):
        obj = super().dict(*args, **kwargs)
        return {
            "tag": obj["tag"],
            "attrs": obj["attrs"],
            "help": obj["help"],
            "elements": obj["elements"],
        }


class Node(NodeBase):
    tag: Optional[str] = ".node"
    attrs: Dict[str, Any] = {}
    help: str = ""
    elements: Union[List, Tuple]

    def __repr__(self):
        meta = ""
        if self.attrs:
            meta += f" {json.dumps(self.attrs, ensure_ascii=False)}"

        if self.help:
            meta += f' "{self.help}"'

        if len(self.elements) < 2:
            it = " ".join(repr(x) for x in self.elements)
            return f"@{self.tag}{meta}({it})"
        else:
            it = " ".join(repr(x) + "\n" for x in self.elements)
            return f"@{self.tag}{meta}(\n {it})"


class RootNode(BaseModel, NodeAbc):
    tag: Optional[str] = Field(".root", const=True)
    attrs: Dict[str, Any] = {}
    help: str = ""
    elements: Union[List, Tuple]

    def one(self):
        undefined = object()
        result = self.one_or(undefined)
        if result is undefined:
            raise RuntimeError()
        else:
            return result

    def one_or(self, default):
        if len(self.__root__) == 0:
            return default
        if len(self.__root__) == 1:
            return self.__root__[0]
        raise RuntimeError()

    __repr__ = __repr__
    __str__ = __str__

    def __iter__(self):
        return iter(self.elements)

    def dict(self, *args, **kwargs):
        obj = super().dict(*args, **kwargs)
        return {
            "tag": obj["tag"],
            "attrs": obj["attrs"],
            "help": obj["help"],
            "elements": obj["elements"],
        }


class ValueNode(NodeBase):
    tag: str = Field(".value", const=True)
    attrs: Dict[str, Any] = {}
    help: str = ""
    elements: conlist(Any, min_items=1, max_items=1)

    @property
    def value(self):
        return self.elements[0]

    def __eq__(self, other) -> bool:
        return self.value == other

    def __repr__(self):
        meta = ""
        if self.attrs:
            meta += f" {json.dumps(self.attrs, ensure_ascii=False)}"

        if self.help:
            meta += f' "{self.help}"'

        if meta:
            return f"@{self.__class__.tag}{meta}({self.value})"
        else:
            return json.dumps(self.value, ensure_ascii=False)

    def __iter__(self):
        yield from ()


class Identifier(NodeBase):
    tag: str = Field(".identifier", const=True)
    attrs: Dict[str, Any] = {}
    help: str = ""
    # elements: Union[List, Tuple]
    elements: List[str]

    def __repr__(self):
        meta = ""
        if self.attrs:
            meta += f" {json.dumps(self.attrs, ensure_ascii=False)}"

        if self.help:
            meta += f' "{self.help}"'

        if meta:
            raise NotImplementedError()
            it = ('"' + x.replace('"', '\\"') + '"' for x in self.elements)
            return f"@{self.__class__.tag}{meta}({' '.join(it)})\n"
        else:
            return repr(self.value)

    @property
    def value(self):
        it = (x.replace('"', '\\"') for x in self.elements)
        return ".".join(it)

    def __iter__(self):
        yield from ()


class Alias(NodeBase):
    tag: str = Field(".alias", const=True)
    attrs: Dict[str, Any] = {}
    help: str = ""
    elements: Union[List, Tuple]

    def __iter__(self):
        yield from ()


class Placeholder(NodeBase):
    tag: str = Field(".placeholder", const=True)
    attrs: Dict[str, Any] = {}
    help: str = ""
    elements: Union[List, Tuple]

    def __iter__(self):
        yield from ()


class Ident:
    ...


class Func:
    name: str

    def evalute(self):
        ...


class From(NodeBase):
    name: str = Field("from", const=True)
    # nodes: Tuple[]


class Join(NodeBase):
    name: str = Field("from", const=True)
    nodes: Tuple[From, "Join"]


class Where(NodeBase):
    name: str = Field("from", const=True)
    nodes: Tuple[Union[From, Join]]


class GroupBy(NodeBase):
    name: str = Field("from", const=True)
    nodes: Tuple[Union[From, Join, Where]]


class Having(NodeBase):
    name: str = Field("from", const=True)
    nodes: Tuple[GroupBy]


class OrderBy(NodeBase):
    name: str = Field("from", const=True)
    nodes: Tuple[Union[From, Join, Where, GroupBy]]


class Select(NodeBase):
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
