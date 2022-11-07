from enum import Flag


class NodeKind(Flag):
    NODE = 0
    ALIAS = 1
    PARAM = 2
    IDENTIFIER = 4


class Node:
    type = NodeKind.NODE

    def __init__(self, *args, **kwargs):
        self.args = args

    @property
    def origin(self):
        return self


class Query(Node):
    def tables(self):
        raise NotImplementedError()


class From(Query):
    def tables(self):
        return self.filter_tables(self.args)

    @staticmethod
    def filter_tables(nodes):
        for x in nodes:
            if x.type & NodeKind.IDENTIFIER:
                if x.type & NodeKind.PARAM:
                    if x.is_binded:
                        yield x.origin
                else:
                    yield x.origin

    def subqueries(self):
        ...


class Join(Query):
    def tables(self):
        yield from self.node.tables()
        yield self.filter_tables([self.args[1]])


class Identifier(str):
    type = NodeKind.IDENTIFIER

    @property
    def origin(self):
        return self


class Alias:
    def __init__(self, identifier, node):
        self.identifier = identifier
        self.node = node

    @property
    def type(self):
        return NodeKind.ALIAS | self.node.type

    @property
    def origin(self):
        return self.node.origin


class Param:
    def __init__(self, identifier, node):
        self.identifier = identifier
        self.node = node

    @property
    def type(self):
        return NodeKind.ALIAS | NodeKind.PARAM | self.node.type

    @property
    def origin(self):
        """For alias and params, get the actual referencing node."""
        return self.node.origin

    @property
    def is_binded(self):
        return hasattr(self, "node")


def test_query_builder():
    assert [x for x in From(Identifier("t1")).tables()] == ["t1"]
    assert [x for x in From(Alias("alias", Identifier("t1"))).tables()] == ["t1"]
    assert [x for x in From(Param("param", Identifier("t1"))).tables()] == ["t1"]
    assert [
        x for x in From(Param("param", Alias("alias", Identifier("t1")))).tables()
    ] == ["t1"]

    # assert [x for x in Join(From(Identifier("t1")), Identifier("t2")).tables()] == [
    #     "t1",
    #     "t2",
    # ]
