from .base import NamedNode
from typing import Dict, List, Tuple


class SqlStatement(NamedNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def build_priority(*priorities: Tuple[str, ...]) -> Dict[str, int]:
    order = {}
    for priority, tags in enumerate(priorities):
        for tag in tags:
            order[tag] = priority
    return order


class Query(SqlStatement):
    name = "query"
    priority = build_priority(
        ("from",),
        ("where",),
        ("group",),
        ("having",),
        ("asc", "desc"),
        ("offset",),
        ("limit",),
        ("select",),
    )

    def sort(self):
        it = (x.name for x in self.elements)
        sorted(it, key=Query.priority.__getitem__)


class Indicator:
    def __init__(self, *tags, maxOccurs=None, minOccurs=None):
        self.tags = tags


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

"""
<?xml version="1.0" ?>
<d:multistatus xmlns:cal="urn:ietf:params:xml:ns:caldav" xmlns:card="urn:ietf:params:xml:ns:carddav" xmlns:cs="http://calendarserver.org/ns/" xmlns:d="DAV:" xmlns:nc="http://nextcloud.org/ns" xmlns:oc="http://owncloud.org/ns" xmlns:s="http://sabredav.org/ns">
<d:response>
<d:href>/remote.php/dav/files/mathias/Invoices/IncomingInvoice.pdf</d:href>
<d:propstat>
<d:prop>
<d:getlastmodified>2017 年 11 月 9 日木曜日 08:28:58 GMT</d:getlastmodified>
<d:getcontentlength>28</d:getcontentlength>
<d:getcontenttype>アプリケーション/pdf</d:getcontenttype>
<oc:permissions>RDNVW</oc:permissions>
<oc:invoicenumber>INV 06–20171112–01</oc:invoicenumber>
<d:resourcetype/>
<d:getetag>"3603cfc90e6db167380fbd524b9af0f3"</d:getetag>
</d:prop>
<d:status>HTTP/ 1.1 200 OK</d:status>
</d:propstat>
</d:response>
</d:multistatus>
"""