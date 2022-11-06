from xml_json import Node


def node(name, *args):
    return Node(name, attrs={}, help="", elements=list(args))


def test_transform():
    """
    dfs(postorder)で処理されること
    http://www-ikn.ist.hokudai.ac.jp/~kida/lecture/alg2019-07.pdf
    """
    # fmt: off
    nodes = node(
        "a",
        node("b",
            node("c",
                node("k")),
            node("d",
                node("g"),
                node("i"))),
        node("e",
            node("f"),
            node("h"),
            node("j")),
    )
    # fmt: on

    assert [x.tag for x in nodes.traverse()] == [
        "k",
        "c",
        "g",
        "i",
        "d",
        "b",
        "f",
        "h",
        "j",
        "e",
        "a",
    ]

    @nodes.traverse
    def traversed(node):
        new_node = node.copy(tag=node.tag * 2)
        return new_node

    assert [x.tag for x in traversed] == [
        "kk",
        "cc",
        "gg",
        "ii",
        "dd",
        "bb",
        "ff",
        "hh",
        "jj",
        "ee",
        "aa",
    ]

    @nodes.transform
    def transformed(node):
        new_node = node.copy(tag=node.tag * 3)
        return new_node

    assert [x.tag for x in transformed.traverse()] == [
        "kkk",
        "ccc",
        "ggg",
        "iii",
        "ddd",
        "bbb",
        "fff",
        "hhh",
        "jjj",
        "eee",
        "aaa",
    ]

    assert [x.tag for x in nodes.traverse_terms()] == [
        "k",
        "g",
        "i",
        "f",
        "h",
        "j",
    ]

    @nodes.transform_terms
    def transformed_terms(node):
        new_node = node.copy(tag=node.tag * 4)
        return new_node

    assert [x.tag for x in transformed_terms.traverse()] == [
        "kkkk",
        "c",
        "gggg",
        "iiii",
        "d",
        "b",
        "ffff",
        "hhhh",
        "jjjj",
        "e",
        "a",
    ]

    assert [x.tag for x in nodes.traverse_terms(where=lambda x: x.tag == "h")] == ["h"]

    assert [
        x.tag
        for x in nodes.transform_terms(
            transformer=lambda x: x.copy(tag=x.tag * 5), where=lambda x: x.tag == "h"
        ).traverse()
    ] == ["k", "c", "g", "i", "d", "b", "f", "hhhhh", "j", "e", "a"]


def test_graph():
    "グラフ用のライブラリとしてNetworkXがある"

    # TODO: onnxモデルからグラフを取得する

    # import networkx as nx

    # G = nx.Graph()
    # G.add_edge("A", "B", weight=4)
    # G.add_edge("B", "D", weight=2)
    # G.add_edge("A", "C", weight=3)
    # G.add_edge("C", "D", weight=4)
    # nx.shortest_path(G, "A", "D", weight="weight")

    # 無向グラフは方向性がない。つまり、エッジは "双方向" の関係を意味する。
    # 有効グラフは方向性がある。つまり、エッジは "方方向" の関係を意味する。

    """
    # networkx.undirected
    @networkx.directed(
        "a":@node(
            "b":@edge(4)
            "c":@edge(3)
        )
        "b":@node(
            "d":@edge(2)
        )
        "c":@node(
            "d":@edge(4)
        )
        "d":@node()
    )
    """

    # topological sortが可能 =  有向非巡回グラフ（DAG）である


"""
query = @from(users)
    :@join(
        groups
        @(users.id == groups.id)
)

@from(query):@select(*)
"""
