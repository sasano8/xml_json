from xml_json.base import AnonymousNode, RootNode, ValueNode


def parse_xml(text):
    from xml.dom.minidom import parseString

    document = parseString(text)
    return create_node(document)


def trim_nodes(nodes):
    from xml.dom.minidom import Text

    for node in nodes:
        if isinstance(node, Text):
            node.data = node.data.strip()
        yield node


def filter_nodes(nodes):
    from xml.dom.minidom import Text

    for node in nodes:
        if isinstance(node, Text):
            if node.data != "":
                yield node
        else:
            yield node


def create_node(node):
    from xml.dom.minidom import Document, Text

    if isinstance(node, Text):
        return ValueNode("", attrs={}, help="", elements=[node.data])
    elif isinstance(node, Document):
        elements = [create_node(x) for x in filter_nodes(trim_nodes(node.childNodes))]
        return RootNode(tag="", attrs={}, help="", elements=elements)
    else:
        elements = [create_node(x) for x in filter_nodes(trim_nodes(node.childNodes))]
        _attrs = node._attrs or {}
        attrs = {k: v._value for k, v in _attrs.items()}
        return AnonymousNode(
            tag=node.tagName.replace(":", "."), attrs=attrs, help="", elements=elements
        )
