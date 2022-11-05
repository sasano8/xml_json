from xml_json import get_parser, JmlTransformer, Identifier, set_debug, Node, parse_xml
import pytest
from lark import Lark

from xml_json.base import ValueNode


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


def test_transform_json(as_json: Lark):
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

    tree = as_element.parse("(QUERY: )")  # TODO: 同じタグで閉じるには？
    assert tree.data == "node"

    with pytest.raises(Exception):
        tree = as_element.parse("1 2")


def test_transform_element(as_element: Lark):
    tf = JmlTransformer()

    tree = as_element.parse("aaa")
    result = tf.transform(tree)
    assert str(result) == "aaa"
    assert isinstance(result, Identifier)

    tree = as_element.parse("aaa.bbb")
    result = tf.transform(tree)
    assert str(result) == "aaa.bbb"
    assert isinstance(result, Identifier)

    tree = as_element.parse("(query: )")
    result = tf.transform(tree)
    assert result.name == "query"
    assert result.attrs == {}
    assert result.help == ""
    assert result.elements == []
    assert isinstance(result, Node)

    tree = as_element.parse('(query {"id": 1} "help": 1 2)')
    result = tf.transform(tree)
    assert result.name == "query"
    assert result.attrs == {"id": 1}
    assert result.help == "help"
    assert result.elements == [1, 2]
    assert isinstance(result, Node)
    assert isinstance(result.elements[0], ValueNode)
    assert isinstance(result.elements[1], ValueNode)


def test_structured_sql(root: Lark):
    """Specification overview."""

    # tree = root.parse("{}")
    # assert tree
    # return

    sql = """
    (query {
        "name": "my model."
    } "this is test query.":
        (or: 1)
        .(or: 2)
        .(or: 3)
        (from: users)
        (groups: groups)
        # from: groups -> *
        # users = from as t
        # users = (from{} "")
        (where:
            {}
            (and: {})
        )
        (groupby: )
        (having: )
        (asc: name)
        (desc: name)
        (offset: 0)
        (limit: +1)
        (select: name)
        (select: "name")
        (select: "age")
        # => x: x + 1;
        # @func(x: str, a: int, d: object): x + 1 and 3;
        # (func() {} "": @(1))
        # @func() {} "": @(1 + 2)
    )
    (query.node:
        aaa.bbb
    )
    """

    """
    (from: users).(where:
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

    tree: Node = root.parse(sql)
    assert tree

    # S式
    # https://ja.wikipedia.org/wiki/S%E5%BC%8F

    # L式
    # http://srfi.schemers.org/srfi-49/srfi-49.html

    # N式
    # http://srfi.schemers.org/srfi-105/srfi-105.html

    # T式
    # http://srfi.schemers.org/srfi-110/srfi-110.html

    from xml_json import Visitor

    tf = JmlTransformer()
    result = tf.transform(tree)
    # for node in Visitor.visit(result):
    #     print(node)
    import pprint

    pprint.pprint(result)


def test_convert_xml_ast():
    import tempfile

    xml = """<?xml version="1.0" encoding="UTF-8"?>
    <d:propfind xmlns:d="DAV:">
        <d:prop xmlns:oc="http://owncloud.org/ns">
            <d:getlastmodified/>
            <d:getcontentlength/>
            <d:getcontenttype/>
            <oc:permissions/>
            <oc:invoicenumber/>
            <d:resourcetype/>
            <d:getetag/>
        </d:prop>
    </d:propfind>"""

    with tempfile.NamedTemporaryFile("r") as tmp:
        with open(tmp.name, "w") as f:
            f.write(xml)

        with open(tmp.name, "r") as f:
            import xml.etree.ElementTree as ET

            tree = ET.parse(f)
            ET.XMLPullParser
            root = tree.getroot()
            # tag: '{DAV:}propfind'
            l, _, r = root.tag.rpartition("}")
            l = l.replace("{", "")
            print(root)

        # with open(tmp.name, "r") as f:
        #     import xml.etree.ElementTree as ET

        #     parser = ET.XMLPullParser()
        #     for line in f.readlines():
        #         parser.feed(line)
        #         for event, elem in parser.read_events():
        #             print(elem)
        #             # if elem.tag == "title":
        #             #     print(elem.text)

    def get_parser(start="start", debug=False):
        with open("xml_json/xml.lark") as grammer:
            return Lark(
                grammer.read(),
                start=start,
                debug=debug,
                # parser="lalr",
                lexer="basic",
                propagate_positions=False,
                maybe_placeholders=False,
            )

    parser = get_parser(debug=True)
    tree = parser.parse(xml)


def test_lark():
    grammer = """
tag_text : /.[^%<>]+?/
// ?elem: "<" "tag"  [CONTENT (CONTENT)*] "<" "tag" "/>"
?elem: [CONTENT*]
TEXT: ">" /.*/ "<"
?start: elem
"""
    # lark = Lark(
    #     grammer,
    #     start="start",
    #     debug=False,
    #     parser="lalr",
    #     # lexer="basic",
    #     propagate_positions=False,
    #     maybe_placeholders=False,
    # )
    # # elem: "<" ">" "<" ">"
    # # tree = lark.parse("asdf#!~|=-@`*+;<>?/!'" + '"\\')  # %
    # # tree = lark.parse("<tag><tag>asdfa<tag/><tag/>")  # %
    # tree = lark.parse(">>asdfa<<")  # %
    # assert tree

    import re

    # xml_pattern = "(?:<.*?>)(.*?)(?:<\\/>)"
    # result = re.findall(xml_pattern, "<>asdf<><>asdfas<>")
    # assert result

    from xml.dom.minidom import parse, parseString

    document = parseString(
        """<?xml version="1.0" encoding="UTF-8"?>
    <d:propfind xmlns:d="DAV:">
        <d:prop xmlns:oc="http://owncloud.org/ns">
            &gt;
            <d:getlastmodified/>
            <d:getcontentlength/>
            <d:getcontenttype/>
            <oc:permissions/>
            <oc:invoicenumber/>
            <d:resourcetype/>
            <d:getetag/>
        </d:prop>
    </d:propfind>"""
    )

    assert document
    document.childNodes[0].tagName  # d:propfind
    document.childNodes[0]._attrs
    document.childNodes[0]._attrs["xmlns:d"]._value
    document.childNodes[0].childNodes[0]  # textnode "'\n        '"
    document.childNodes[0].childNodes[1]  # d:prop
    document.childNodes[0].childNodes[1].childNodes[
        0
    ].data  # '\n            >\n            '


# defusedxml
# python標準のxmlライブラリでは脆弱性があるため、セキュリティを気にする場合はdefusedxmlを使用する

# SAX(Simple API for XML)
# xmlを解析し、イベント化する
"""

SetDocumentLocator
StartDocument
StartElement :ブックリスト
StartElement :アイテム (id=11111)
StartElement :タイトル
Characters :鹿子木といえばXML
EndElement :タイトル
StartElement :筆者
Characters :鹿子木亨紀
EndElement :筆者
StartElement :カテゴリ
Characters :1
EndElement :カテゴリ
EndElement :アイテム
StartElement :アイテム (id=22222)
StartElement :タイトル
Characters :丸橋によるXML講座
EndElement :タイトル
StartElement :筆者
Characters :丸橋玲奈
EndElement :筆者
StartElement :カテゴリ
Characters :2
EndElement :カテゴリ
EndElement :アイテム
StartElement :アイテム (id=33333)

……中略……

EndElement :アイテム
EndElement :ブックリスト
EndDocument
"""


def test_parse_from_xml():
    tree = parse_xml(
        """<?xml version="1.0" encoding="UTF-8"?>
    <d:propfind xmlns:d="DAV:">
        <d:prop xmlns:oc="http://owncloud.org/ns">
            &gt;
            <d:getlastmodified/>
            <d:getcontentlength/>
            <d:getcontenttype/>
            <oc:permissions/>
            <oc:invoicenumber/>
            <d:resourcetype/>
            <d:getetag/>
        </d:prop>
    </d:propfind>"""
    )
    assert (
        str(tree).replace(" ", "").replace("\n", "")
        == """
        (d.propfind {"xmlns:d": "DAV:"}: (d.prop {"xmlns:oc": "http://owncloud.org/ns"}:
        ">"
        (d.getlastmodified: )
        (d.getcontentlength: )
        (d.getcontenttype: )
        (oc.permissions: )
        (oc.invoicenumber: )
        (d.resourcetype: )
        (d.getetag: )
        ))""".replace(
            " ", ""
        ).replace(
            "\n", ""
        )
    )


"""
* = (from: users)
* = users -> from
t1 = groups -> from
users = (from: $)
groups = (from: (select: $))


(select :
    from: users -> *
    # groups -> from

    # JOIN t2 ON t1.user_id = t2.user_id
    # JOIN t3 ON t1.user_id = t3.user_id

    t2 = groups -> join.on: @(users.group_id == t2.group_id)
    t3 = groups -> join -> on: @(users.group_id == t3.group_id)
    t4 = groups -> join -> using: emp_no

    join: groups@t2 @(users.group_id == t2.group_id)

    join.on: groups -> t2 @(users.group_id == t2.group_id)
    t3 <- join.using: groups emp_no

    this.where(@(
        users == 1
    ))
)
"""

"""
(from:
    users
).(join.on:
    groups
    @(users.group_id == groups.id)
).(join.using:
    groups
    emp_no
).(groupby: group)
.(orderby: 1)
.(limit: 1)
).(select:
    name
)

(from:).(select:
    1
)
"""


"""
@query(
    @from{
        "": "aaaaaaaaaaaaaaaaaaaa"
    }(
        users
    ):@join(
        groups,
        users.id == groups.id
    )
):@select{
    "": "asdfddddddddddddddddddddd"
}(
    id
    name
)
"""


def querable(func):
    ...


class ParamError(Exception):
    ...


@querable
def func(source, id):
    """
    @from(
        users = $source
    )
    :@join(
        groups
        users.id == groups.id
    )
    :@where(
        users.id == $id: str
    )
    :@select(
        id -> user_id
        name
    ) -> t1
    """
    if id != "dsadfa":
        raise ParamError("id", "")


def query(*args):
    ...


class Identifiered:
    def __init__(self, *args):
        ...

    # """
    # @from(
    #     users = $source
    # )
    # :@join(
    #     groups
    #     users.id == groups.id
    # )
    # :@where(
    #     users.id == $id: str
    # )
    # :@select(
    #     id -> user_id
    #     name
    # ) -> t1
    # """,
    # source=Identifiered("asdfa"),
    # id="sadfas",


"""
@from(
    users
)
:@join(
    groups
    users.id == users.id
)
:@where(
    users.id == $id: str
    users.id and groups.id
)
:@select(
    users.id
    users.name
) -> t1
"""
