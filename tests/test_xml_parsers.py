from xml_json import Node
from xml_json.parsers import xml as xml_parser

"""
順序インジケータ:
    All: 要素が順不同に現れることができ、 且つ、各子要素は一度だけ発生しなければならない
    Choice: 1つの子要素または他のものが発生する可能性がある
    Sequence: 子要素が指定の順序で出現する必要のある
発生インジケータ（属性）:
    maxOccurs: 要素が発生できる最大回数
    minOccurs: 要素が発生することができる最小の数
グループインジケータ:
    Group name:
    attributeGroup name:
"""


"""
curl -u 'username:password' 'https://mynextcloud/remote.php/dav/files/mathias/Invoices/IncomingInvoice.pdf' -X PROPFIND - data '<?xml version="1.0" encoding="UTF-8"?><d:propfind xmlns:d="DAV:"><d:prop xmlns:oc="http://owncloud.org/ns"><d:getlastmodified/><d:getcontentlength/><d:getcontenttype/><oc:permissions/><oc:invoicenumber/><d:resourcetype/><d:getetag/></d:prop></d:propfind>'
"""


def test_parse_from_xml():

    # TODO: python標準のxmlライブラリでは脆弱性があるため、セキュリティを気にする場合はdefusedxmlを使用する

    from xml.dom.minidom import parseString

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

    node = document.childNodes[0]
    Node(
        node.tagName,
        {k: v.value for k, v in node._attrs.items()},
        "",
        [node.childNodes[0], node.childNodes[1]],
    )

    tree = xml_parser.parse_xml(
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
        @d.propfind {"xmlns:d": "DAV:"}(
            @d.prop {"xmlns:oc": "http://owncloud.org/ns"}(
                ">"
                @d.getlastmodified()
                @d.getcontentlength()
                @d.getcontenttype()
                @oc.permissions()
                @oc.invoicenumber()
                @d.resourcetype()
                @d.getetag()
        ))""".replace(
            " ", ""
        ).replace(
            "\n", ""
        )
    )
