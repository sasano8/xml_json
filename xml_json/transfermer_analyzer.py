from .parser import (
    JmlTransformer,
    NODE_VALUE,
    NODE_IDENTIFIER,
    NODE_ANONYMOUS,
    NODE_ALIAS,
    NODE_PLACEHOLDER,
    NODE_EXPRESSION,
)


class TransformeAnalyzerBase:
    def __init__(self, transformer: JmlTransformer):
        self.root = transformer
        self.must_validate()
        self.validate()

    def must_validate(self):
        if NODE_VALUE not in self.root.mapper:
            raise Exception(f"'{NODE_VALUE}' must be supported.")

    def validate(self):
        ...

    def get_spec(self):
        return dict(self._get_spec(name) for name in self.get_spec_names())

    @classmethod
    def get_spec_names(cls):
        return [
            "is_case_sensitive",
            "is_allow_identifier",
            "is_allow_anonymous_node",
            "is_allow_alias",
            "is_allow_placeholder",
            "is_allow_expression",
        ]

    def _get_spec(self, name):
        func = getattr(self, name)
        return (name, func())

    def is_allow_identifier(self):
        return NODE_IDENTIFIER in self.root.mapper

    def is_allow_anonymous_node(self):
        return NODE_ANONYMOUS in self.root.mapper

    def is_allow_alias(self):
        return NODE_ALIAS in self.root.mapper

    def is_allow_placeholder(self):
        return NODE_PLACEHOLDER in self.root.mapper

    def is_allow_expression(self):
        return NODE_EXPRESSION in self.root.mapper

    def is_case_sensitive(self):
        allow_lower = NODE_VALUE.lower() in self.root.mapper
        allow_upper = NODE_VALUE.upper() in self.root.mapper

        if all([allow_lower, allow_upper]):
            return "lower/upper"

        if allow_lower:
            return "lower"

        if allow_upper:
            return "upper"

        raise Exception()


class TransformeAnalyzer(TransformeAnalyzerBase):
    def validate(self):
        ...
