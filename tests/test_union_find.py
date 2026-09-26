import pytest
from src.union_find import UnionFind


def test_basic_union():
    uf = UnionFind(5)
    uf.union(0, 1)
    assert uf.connected(0, 1)
    assert not uf.connected(0, 2)


def test_transitive_union():
    uf = UnionFind(5)
    uf.union(0, 1)
    uf.union(1, 2)
    assert uf.connected(0, 2)


def test_find_rejects_negative_index():
    uf = UnionFind(5)
    with pytest.raises(ValueError):
        uf.find(-1)


def test_find_rejects_out_of_range_index():
    uf = UnionFind(5)
    with pytest.raises(ValueError):
        uf.find(5)
