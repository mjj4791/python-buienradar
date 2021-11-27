"""Basic testing for CLI."""
from buienradar.buienradar_json import __to_upper


def test_to_upper():
    """Test the __to_upper function."""
    inout = [
        {"in": "", "out": ""},
        {"in": " ", "out": " "},
        {"in": None, "out": None},
        {"in": 123, "out": 123},
        {"in": 123.4, "out": 123.4},
        {"in": "A", "out": "A"},
        {"in": "AB", "out": "AB"},
        {"in": "ABC", "out": "ABC"},
        {"in": "a", "out": "A"},
        {"in": "ab", "out": "AB"},
        {"in": "abc", "out": "ABC"},
        {"in": "AbcaBcabC", "out": "ABCABCABC"}
    ]
    for val in inout:
        result = __to_upper(val['in'])
        assert result == val['out']
