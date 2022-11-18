import pytest

from xml_json import JmlTransformer
from xml_json.transfermer_analyzer import TransformeAnalyzerBase


def test_transfermer_analyzer():
    with pytest.raises(Exception, match="'.value' must be supported"):
        t1 = JmlTransformer(mapper={})
        TransformeAnalyzerBase(t1).get_spec()

    def analyze(x):
        mapper = dict.fromkeys(x, None)
        return TransformeAnalyzerBase(JmlTransformer(mapper=mapper)).get_spec()

    if spec := analyze({".value"}):
        assert spec
        assert spec["is_case_sensitive"] == "lower"
        # {
        #     "is_allow_identifier": False,
        #     "is_allow_anonymous_node": False,
        #     "is_case_sensitive": "lower",
        #     "is_allow_alias": False,
        #     "is_allow_placeholder": False,
        # }

    if spec := analyze({".value", ".node"}):
        assert spec["is_allow_anonymous_node"]

    if spec := analyze({".value", ".identifier"}):
        assert spec["is_allow_identifier"]

    if spec := analyze({".value", ".alias"}):
        assert spec["is_allow_alias"]

    if spec := analyze({".value", ".placeholder"}):
        assert spec["is_allow_placeholder"]

    if spec := analyze({".value", ".expr"}):
        assert spec["is_allow_expression"]

    if spec := analyze({".value", ".call"}):
        assert spec["is_allow_call"]
