import json
from copy import deepcopy


class Node:
    export = False  # export alias

    def __init__(self, name, attrs, help, elements):
        self.name = name
        self.attrs = {} if attrs is None else attrs
        self.help = "" if help is None else help
        self.elements = elements

    def __copy__(self, name=None, attrs=None, help=None, elements=None):
        kwargs = {
            "name": name or self.name,
            "attrs": attrs or deepcopy(self.attrs),
            "help": help or self.help,
            "elements": elements or list(self.elements),
        }
        return self.__class__(**kwargs)

    copy = __copy__

    def __iter__(self):
        return self.elements.__iter__()

    def __repr__(self):
        meta = ""
        if self.attrs:
            meta += f" {json.dumps(self.attrs, ensure_ascii=False)}"

        if self.help:
            meta += f' "{self.help}"'

        if len(self.elements) < 2:
            it = " ".join(repr(x) for x in self.elements)
            return f"({self.name}{meta}: {it})"
        else:
            it = " ".join(repr(x) + "\n" for x in self.elements)
            return f"({self.name}{meta}:\n {it})"

    @property
    def identifiers(self):
        ...

    @property
    def params(self):
        ...

    def traverse(self, transformer=None):
        transformer = transformer or (lambda x: x)
        for elm in self.elements:
            yield from elm.traverse(transformer)
        yield transformer(self)

    def transform(self, transformer=None):
        transformer = transformer or (lambda x: x)
        elements = [x.transform(transformer) for x in self.elements]
        new_node = self.copy(elements=elements)
        return transformer(new_node)

    def traverse_terms(self, transformer=None, where=None):
        transformer = transformer or (lambda x: x)
        where = where or (lambda x: True)
        if self.elements:
            for elm in self.elements:
                yield from elm.traverse_terms(transformer, where)
        else:
            if where(self):
                yield transformer(self)
            # else:
            #     yield self

    def transform_terms(self, transformer=None, where=None):
        transformer = transformer or (lambda x: x)
        where = where or (lambda x: True)
        if self.elements:
            elements = [x.transform_terms(transformer, where) for x in self.elements]
            return self.copy(elements=elements)
        else:
            if where(self):
                return transformer(self)
            else:
                return self

    def analyze(self, parent, ctx):
        ...

    def bind(self, *args, **kwargs):
        ...

    def resolve(self, filter, resolver):
        ...


class AnonymousNode(Node):
    ...


class TermNode:
    def __iter__(self):
        yield from ()

    def __repr__(self):
        raise NotImplementedError()


class NamedNode(Node):
    name: str

    def __init__(self, name, attrs, help, elements):
        Node.__init__(self, self.__class__.name, attrs, help, elements)


class RootNode(NamedNode):
    name = "root"

    def __repr__(self):
        meta = ""
        if self.attrs:
            meta += f" {json.dumps(self.attrs, ensure_ascii=False)}"

        if self.help:
            meta += f' "{self.help}"'

        if len(self.elements) < 2:
            it = " ".join(repr(x) for x in self.elements)
            return it
        else:
            it = " ".join(repr(x) + "\n" for x in self.elements)
            return it


class ValueNode(TermNode, NamedNode):
    name = "json"

    def __init__(self, name, attrs, help, elements):
        if len(elements) != 1:
            raise ValueError()
        Node.__init__(self, self.__class__.name, attrs, help, elements)

    @property
    def value(self):
        return self.elements[0]

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        meta = ""
        if self.attrs:
            meta += f" {json.dumps(self.attrs, ensure_ascii=False)}"

        if self.help:
            meta += f' "{self.help}"'

        if meta:
            return f"({self.__class__.name}{meta}: {self.value})"
        else:
            return json.dumps(self.value, ensure_ascii=False)

    def __eq__(self, other) -> bool:
        return self.value == other


class Identifier(TermNode, NamedNode):
    name = "identifier"

    # def __init__(self, *args):
    #     self._children = args

    def __init__(self, name, attrs, help, elements):
        if len(elements) < 1:
            raise ValueError()
        if not all(isinstance(x, str) for x in elements):
            raise ValueError()

        Node.__init__(self, self.__class__.name, attrs, help, elements)

    def __getitem__(self, i):
        return self.elements[i]

    def __len__(self):
        return len(self.elements)

    def __str__(self):
        return ".".join(self.elements)

    def __repr__(self):
        meta = ""
        if self.attrs:
            meta += f" {json.dumps(self.attrs, ensure_ascii=False)}"

        if self.help:
            meta += f' "{self.help}"'

        if meta:
            it = ('"' + x.replace('"', '\\"') + '"' for x in self.elements)
            return f"({self.__class__.name}{meta}: {' '.join(it)})\n"
        else:
            return self.value

    def __eq__(self, other) -> bool:
        return str(self) == other

    @property
    def value(self):
        it = (x.replace('"', '\\"') for x in self.elements)
        return ".".join(it)
