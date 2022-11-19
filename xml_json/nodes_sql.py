from typing import Dict, Tuple

from .base import NamedNode


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
