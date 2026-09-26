import pytest
from src.lru_cache import LRUCache


def test_basic_get_put():
    c = LRUCache(2)
    c.put(1, "a")
    c.put(2, "b")
    assert c.get(1) == "a"


def test_eviction_removes_least_recently_used():
    c = LRUCache(2)
    c.put(1, "a")
    c.put(2, "b")
    c.get(1)       # 1 is now most-recently-used, 2 is least
    c.put(3, "c")  # should evict 2, keep 1 and 3
    assert c.get(1) == "a"
    assert c.get(2) == -1
    assert c.get(3) == "c"


def test_zero_capacity_rejected():
    with pytest.raises(ValueError):
        LRUCache(0)
