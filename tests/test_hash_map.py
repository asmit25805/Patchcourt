import pytest
from src.hash_map import HashMap


def test_put_get():
    h = HashMap()
    h.put("a", 1)
    assert h.get("a") == 1


def test_overwrite():
    h = HashMap()
    h.put("a", 1)
    h.put("a", 2)
    assert h.get("a") == 2


def test_missing_key_raises():
    h = HashMap()
    with pytest.raises(KeyError):
        h.get("missing")
