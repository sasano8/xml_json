import pytest
from lark import Lark

from xml_json import (
    Identifier,
    JmlTransformer,
    Node,
    get_parser,
    set_debug,
    ValueNode,
)


@pytest.fixture
def root():
    # set_debug()
    return get_parser(start="start")


@pytest.fixture
def as_json():
    set_debug()
    return get_parser(start="json")


@pytest.fixture
def as_element():
    set_debug()
    return get_parser(start="element")


def test_json_transformer(as_json: Lark):
    tf = JmlTransformer()

    tree = as_json.parse("1")
    assert tf.transform(tree) == 1.0

    tree = as_json.parse('""')
    assert tf.transform(tree) == ""

    tree = as_json.parse('"a"')
    assert tf.transform(tree) == "a"

    tree = as_json.parse(r'"a\""')
    assert tf.transform(tree) == 'a"'

    with pytest.raises(Exception):
        tree = as_json.parse("''")

    tree = as_json.parse("true")
    assert tf.transform(tree) == True

    tree = as_json.parse("false")
    assert tf.transform(tree) == False

    tree = as_json.parse("null")
    assert tf.transform(tree) == None

    tree = as_json.parse("[]")
    result = tf.transform(tree)
    assert result == []
    assert isinstance(result, list)

    tree = as_json.parse("[1]")
    result = tf.transform(tree)
    assert result == [1]
    assert isinstance(result, list)

    tree = as_json.parse("{}")
    result = tf.transform(tree)
    assert result == {}
    assert isinstance(result, dict)

    tree = as_json.parse('{"val": 1}')
    result = tf.transform(tree)
    assert result == {"val": 1}
    assert isinstance(result, dict)

    with pytest.raises(Exception):
        tree = as_json.parse("1 2")


def test_parse_element(as_element: Lark):
    tree = as_element.parse("1")
    assert tree.data == "int"

    tree = as_element.parse("1.0")
    assert tree.data == "float"

    tree = as_element.parse('""')
    assert tree.data == "string"

    tree = as_element.parse("true")
    assert tree.data == "true"

    tree = as_element.parse("false")
    assert tree.data == "false"

    tree = as_element.parse("null")
    assert tree.data == "null"

    tree = as_element.parse("[]")
    assert tree.data == "array"

    tree = as_element.parse("{}")
    assert tree.data == "object"

    tree = as_element.parse("aaa")
    assert tree.data == "identifier"

    tree = as_element.parse("aaa.bbb")
    assert tree.data == "identifier"

    tree = as_element.parse("@ QUERY()")
    assert tree.data == "node"

    tree = as_element.parse("$a")
    assert tree.data == "param"

    with pytest.raises(Exception):
        tree = as_element.parse("$ a")

    tree = as_element.parse("$a: int")
    assert tree.data == "param"

    tree = as_element.parse("$a: int = null")
    assert tree.data == "param"

    tree = as_element.parse("aaa.bbb = 1")
    assert tree.data == "alias"

    with pytest.raises(Exception):
        tree = as_element.parse("1 2")


def test_transform_element(as_element: Lark):
    tf = JmlTransformer(
        mapper={".node": Node, ".value": ValueNode, ".identifier": Identifier}
    )

    tree = as_element.parse("aaa")
    result = tf.transform(tree)
    assert str(result) == "aaa"
    assert isinstance(result, Identifier)

    tree = as_element.parse("aaa.bbb")
    result = tf.transform(tree)
    assert str(result) == "aaa.bbb"
    assert isinstance(result, Identifier)

    tree = as_element.parse("@query()")
    result = tf.transform(tree)
    assert result.tag == "query"
    assert result.attrs == {}
    assert result.help == ""
    assert result.elements == []
    assert isinstance(result, Node)

    tree = as_element.parse('@query {"id": 1} "help"(1 2)')
    result = tf.transform(tree)
    assert result.tag == "query"
    assert result.attrs == {"id": 1}
    assert result.help == "help"
    assert result.elements == [1, 2]
    assert isinstance(result, Node)
    assert isinstance(result.elements[0], ValueNode)
    assert isinstance(result.elements[1], ValueNode)


def test_structured_sql(root: Lark):
    """Specification overview."""

    sql = """
    @query1 {
        "name": "my model."
    } "this is test query."(
        @or(1)
        :@or(2)
        :@or(3)
        @from(users)
        @groups(groups)
        # from: groups -> *
        # users = from as t
        # users = (from{} "")
        @where(
            {}
            @and({})
        )
        @groupby()
        @having()
        @asc(name)
        @desc(name)
        @offset(0)
        @limit(+1)
        @select(name)
        @select("name")
        @select("age")
        # => x: x + 1;
        # @func(x: str, a: int, d: object): x + 1 and 3;
        # (func() {} "": @(1))
        # @func() {} "": @(1 + 2)
    )
    @query2.node(
        aaa.bbb
    )
    """

    """
    @from(users):@where(
        x => @(
            x.id == 1 and x.group == 1
        )
    )
    """

    # sql = """(and: 1).(and: 2).(and: 3)"""

    priority = [
        "from",
        "where",
        "group",
        "having",
        ("asc", "desc"),
        "offset",
        "limit",
        "select",
    ]

    tree = root.parse(sql)
    assert tree

    # S式
    # https://ja.wikipedia.org/wiki/S%E5%BC%8F

    # L式
    # http://srfi.schemers.org/srfi-49/srfi-49.html

    # N式
    # http://srfi.schemers.org/srfi-105/srfi-105.html

    # T式
    # http://srfi.schemers.org/srfi-110/srfi-110.html

    tf = JmlTransformer(
        mapper={".node": Node, ".value": ValueNode, ".identifier": Identifier}
    )
    result = tf.transform(tree)
    import pprint

    pprint.pprint(result)
    assert [x.tag for x in result] == ["query1", "query2.node"]


def test_onnx():
    import onnnx

    onnnx.main()
