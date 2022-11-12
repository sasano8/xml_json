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


NODE_ANONYMOUS = ".node"
NODE_IDENTIFIER = ".identifier"
NODE_VALUE = ".value"
NODE_ALIAS = ".alias"
NODE_PLACEHOLDER = ".placeholder"
NODE_EXPRESSION = ".expr"


class JmlTransformer(JsonTransformer):
    def __init__(self, mapper: dict = {}):
        self.mapper = mapper

    def identifier(self, tree):
        return self.map(NODE_IDENTIFIER, {}, "", tree)

    def root(self, tree):
        return RootNode("", {}, "", tree[0])

    def elements(self, tree):
        result = [
            x if isinstance(x, Node) else self.map(NODE_VALUE, {}, "", [x])
            for x in tree
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
        return self.map(NODE_VALUE, {}, "", tree)

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
            try:
                cls = self.mapper[NODE_ANONYMOUS]
                return cls(name, attrs, help, elements)
            except KeyError:
                raise GrammarError(f"Not supported anonymous tag: {name}")
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
