import os
from typing import Type, Union

from lark import Lark, Transformer, v_args
from lark.exceptions import GrammarError

from .base import AnonymousNode, Identifier, Node, RootNode, ValueNode

path = os.path.dirname(__file__)


class JsonTransformer(Transformer):
    @v_args(inline=True)
    def string(self, tree):
        return tree[1:-1].replace('\\"', '"')

    # number = v_args(inline=True)(float)
    int = v_args(inline=True)(int)
    float = v_args(inline=True)(float)
    true = lambda self, _: True
    false = lambda self, _: False
    null = lambda self, _: None
    array = list
    pair = tuple
    object = dict


def not_support_anonymous(*args, **kwargs):
    raise NotImplementedError()


IDENTIFIER = "identifier"
VALUE = "value"


class JmlTransformer(JsonTransformer):
    def __init__(
        self,
        mapper: dict = None,
        # anonymous: Union[Type[Node], None] = AnonymousNode,
        # case_sensitive: bool = True,  # TODO: 実装する
        # allow_anonymous: bool = True,
    ):
        self.mapper = mapper or {}
        # self.anonymous = not_support_anonymous if anonymous is None else anonymous

    def identifier(self, tree):
        # return Identifier("", {}, "", list(str(x).lower() for x in tree))
        # elements = [str(x).lower() for x in tree]
        return self.map(IDENTIFIER, {}, "", tree)

    def root(self, tree):
        return RootNode("", {}, "", tree[0])

    def elements(self, tree):
        # normalize = (
        #     lambda x: x if isinstance(x, Node) else self.map("value", {}, "", [x])
        # )
        result = [
            x if isinstance(x, Node) else self.map(VALUE, {}, "", [x]) for x in tree
        ]
        return result

    def attrs(self, tree):
        if tree:
            return tree[0]
        else:
            return {}

    def help(self, tree):
        if tree:
            return tree[0]
        else:
            return ""

    def json_node(self, tree):
        return self.map(VALUE, {}, "", tree)

    def node(self, tree):
        root = self.create_node(tree)
        current = root

        for i in range(len(tree) - 4):
            parent = tree[4 + i].children
            parent[3].insert(0, current)
            current = self.create_node(parent)

        return current

    def create_node(self, tree):
        name = str(tree[0])
        attrs = tree[1]
        help = tree[2]
        elements = tree[3]
        return self.map(name, attrs, help, elements)

    def map(self, name, attrs, help, elements):
        try:
            cls = self.mapper[name]
        except KeyError:
            raise GrammarError(f"Not supported tag: {name}")
        return cls(name, attrs, help, elements)


class JmlAllowAnonymousNodeTransformer(JmlTransformer):
    def map(self, name, attrs, help, elements):
        try:
            cls = self.mapper[name]
        except KeyError:
            cls = self.mapper["node"]
        return cls(name, attrs, help, elements)


import logging


def set_debug():
    from lark import logger

    logger.setLevel(logging.DEBUG)


def get_parser(start="start", debug=False):
    with open(path + "/xml_json.lark") as grammer:
        return Lark(
            grammer.read(),
            start=start,
            debug=debug,
            parser="lalr",
            # lexer="basic",
            propagate_positions=False,
            maybe_placeholders=False,
        )


def parse(text: str):
    parser = get_parser()
    tree = parser.parse(text)
    # result = SqlTransformer().transform(tree)
    result = tree
    return result


def beautify():
    ...


def minify():
    ...


def build(
    parser,
):
    ...


class Visitor:
    @staticmethod
    def visit(node: Node, depth=0):
        for child in node:
            yield from Visitor.visit(child, depth + 1)
            # yield (depth, child)
            yield child


# def parse_xml(text):
#     from xml.dom.minidom import parse, parseString

#     document = parseString(text)
#     return create_node(document)


# def trim_nodes(nodes):
#     from xml.dom.minidom import Text

#     for node in nodes:
#         if isinstance(node, Text):
#             node.data = node.data.strip()
#         yield node


# def filter_nodes(nodes):
#     from xml.dom.minidom import Text

#     for node in nodes:
#         if isinstance(node, Text):
#             if node.data != "":
#                 yield node
#         else:
#             yield node


# def analyze_node(node):
#     ...


# def create_root_node(node):
#     return create_node(node)


# def create_node(node):
#     from xml.dom.minidom import Document, Text

#     if isinstance(node, Text):
#         return ValueNode("", attrs={}, help="", elements=[node.data])
#     elif isinstance(node, Document):
#         elements = [create_node(x) for x in filter_nodes(trim_nodes(node.childNodes))]
#         return RootNode(tag="", attrs={}, help="", elements=elements)
#     else:
#         elements = [create_node(x) for x in filter_nodes(trim_nodes(node.childNodes))]
#         _attrs = node._attrs or {}
#         attrs = {k: v._value for k, v in _attrs.items()}
#         return AnonymousNode(
#             tag=node.tagName.replace(":", "."), attrs=attrs, help="", elements=elements
#         )
