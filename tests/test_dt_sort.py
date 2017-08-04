#!/usr/bin/env python3
# Copyright 2017 H2O.ai; Apache License Version 2.0;  -*- encoding: utf-8 -*-
import datatable
import pytest
import random



#-------------------------------------------------------------------------------

def test_i4i_small():
    d0 = datatable.DataTable([17, 2, 96, 245, 847569, 34, -45, None, 1])
    assert d0.stypes == ("i4i", )
    d1 = d0(sort=0)
    assert d1.stypes == d0.stypes
    assert d1.internal.isview
    assert d1.internal.check()
    assert d1.topython() == [[None, -45, 1, 2, 17, 34, 96, 245, 847569]]


def test_i4i_small_stable():
    d0 = datatable.DataTable([
        [5, 3, 5, None, 1000000, None, 3, None],
        [1, 5, 10, 20, 50, 100, 200, 500]
    ], colnames=["A", "B"])
    d1 = d0(sort="A")
    assert d1.internal.check()
    assert d1.topython() == [
        [None, None, None, 3, 3, 5, 5, 1000000],
        [20, 100, 500, 5, 200, 1, 10, 50],
    ]


def test_i4i_large():
    # p1, p2 should both be prime, with p1 < p2. Here we rely on the fact that
    # a multiplicative group of integers module n is cyclic with order n-1 when
    # n is prime.
    p1 = 1000003
    p2 = 2000003
    src = [((n + 1) * p2) % p1 for n in range(p1)]
    d0 = datatable.DataTable(src)
    assert d0.stypes == ("i4i", )
    d1 = d0(sort=0)
    assert d1.topython() == [list(range(p1))]


@pytest.mark.parametrize("n", [30, 300, 3000, 30000, 60000, 120000])
def test_i4i_large_stable(n):
    src = [None, 100, 100000] * (n // 3)
    d0 = datatable.DataTable({"A": src, "B": list(range(n))})
    assert d0.stypes[0] == "i4i"
    d1 = d0(sort="A", select="B")
    assert d1.topython() == [list(range(0, n, 3)) +
                             list(range(1, n, 3)) +
                             list(range(2, n, 3))]


@pytest.mark.parametrize("n", [5, 100, 500, 2500, 32767, 32768, 32769, 200000])
def test_i4i_constant(n):
    tbl0 = [[100000] * n, list(range(n))]
    d0 = datatable.DataTable(tbl0)
    assert d0.stypes[0] == "i4i"
    d1 = d0(sort=0)
    assert d1.stypes == d0.stypes
    assert d1.topython() == tbl0


def test_i4i_reverse():
    step = 10
    d0 = datatable.DataTable(list(range(1000000, 0, -step)))
    assert d0.stypes[0] == "i4i"
    d1 = d0(sort=0)
    assert d1.stypes == d0.stypes
    assert d1.topython() == [list(range(step, 1000000 + step, step))]


@pytest.mark.parametrize("b", [32767, 1000000])
def test_i4i_upper_range(b):
    # This test looks at an i4 array with small range but large absolute values.
    # After subtracting the mean it will be converted into uint16_t for sorting,
    # and we test here that such conversion gives the correct results.
    d0 = datatable.DataTable([b, b - 1, b + 1] * 1000)
    assert d0.stypes[0] == "i4i"
    d1 = d0(sort=0)
    assert d1.topython() == [[b - 1] * 1000 + [b] * 1000 + [b + 1] * 1000]


@pytest.mark.parametrize("dc", [32765, 32766, 32767, 32768,
                                65533, 65534, 65535, 65536])
def test_i4i_u2range(dc):
    # Test array with range close to 2^15 / 2^16 (looking for potential off-by-1
    # errors at the boundary of int16_t / uint16_t)
    a = 100000
    b = a + 10
    c = a + dc
    d0 = datatable.DataTable([c, b, a] * 1000)
    assert d0.stypes[0] == "i4i"
    d1 = d0(sort=0)
    assert d1.topython() == [[a] * 1000 + [b] * 1000 + [c] * 1000]


def test_i4i_unsigned():
    # In this test the range of values is 32 bits, so that after removing the
    # radix we would have full 16 bits remaining. At that point we should be
    # careful not to conflate unsigned sorting with signed sorting.
    tbl = sum(([t] * 100 for t in [0x00000000, 0x00000001, 0x00007FFF,
                                   0x00008000, 0x00008001, 0x0000FFFF,
                                   0x7FFF0000, 0x7FFF0001, 0x7FFF7FFF,
                                   0x7FFF8000, 0x7FFF8001, 0x7FFFFFFF]), [])
    d0 = datatable.DataTable(tbl)
    assert d0.stypes == ("i4i", )
    d1 = d0(sort=0)
    assert d1.internal.check()
    assert d1.topython() == [tbl]


def test_i4i_issue220():
    d0 = datatable.DataTable([None] + [1000000] * 200 + [None])
    d1 = d0(sort=0)
    assert d1.topython() == [[None, None] + [1000000] * 200]



#-------------------------------------------------------------------------------

def test_i1i_small():
    d0 = datatable.DataTable([17, 2, 96, 45, 84, 75, 69, 34, -45, None, 1])
    assert d0.stypes == ("i1i", )
    d1 = d0(sort=0)
    assert d1.stypes == d0.stypes
    assert d1.internal.isview
    assert d1.internal.check()
    assert d1.topython() == [[None, -45, 1, 2, 17, 34, 45, 69, 75, 84, 96]]


def test_i1i_small_stable():
    d0 = datatable.DataTable([
        [5, 3, 5, None, 100, None, 3, None],
        [1, 5, 10, 20, 50, 100, 200, 500]
    ], colnames=["A", "B"])
    d1 = d0(sort="A")
    assert d1.internal.check()
    assert d1.topython() == [
        [None, None, None, 3, 3, 5, 5, 100],
        [20, 100, 500, 5, 200, 1, 10, 50],
    ]


def test_i1i_large():
    d0 = datatable.DataTable([(i * 1327) % 101 - 50 for i in range(1010)])
    d1 = d0(sort=0)
    assert d1.stypes == ("i1i", )
    assert d1.internal.check()
    assert d1.topython() == [sum(([i] * 10 for i in range(-50, 51)), [])]


@pytest.mark.parametrize("n", [30, 303, 3333, 30000, 60009, 120000])
def test_i1i_large_stable(n):
    src = [None, 10, -10] * (n // 3)
    d0 = datatable.DataTable({"A": src, "B": list(range(n))})
    assert d0.stypes[0] == "i1i"
    d1 = d0(sort="A", select="B")
    assert d1.topython() == [list(range(0, n, 3)) +
                             list(range(2, n, 3)) +
                             list(range(1, n, 3))]



#-------------------------------------------------------------------------------

def test_i1b_small():
    d0 = datatable.DataTable([True, False, False, None, True, True, None])
    assert d0.stypes == ("i1b", )
    d1 = d0(sort="C1")
    assert d1.stypes == d0.stypes
    assert d1.internal.isview
    assert d1.internal.check()
    assert d1.topython() == [[None, None, False, False, True, True, True]]


def test_i1b_small_stable():
    d0 = datatable.DataTable([[True, False, False, None, True, True, None],
                              [1, 2, 3, 4, 5, 6, 7]])
    assert d0.stypes == ("i1b", "i1i")
    d1 = d0(sort="C1")
    assert d1.stypes == d0.stypes
    assert d1.names == d0.names
    assert d1.internal.isview
    assert d1.internal.check()
    assert d1.topython() == [[None, None, False, False, True, True, True],
                             [4, 7, 2, 3, 1, 5, 6]]


@pytest.mark.parametrize("n", [100, 512, 1000, 5000, 100000])
def test_i1b_large(n):
    d0 = datatable.DataTable([True, False, True, None, None, False] * n)
    assert d0.stypes == ("i1b", )
    d1 = d0(sort=0)
    assert d1.stypes == d0.stypes
    assert d1.names == d0.names
    assert d1.internal.isview
    assert d1.internal.check()
    nn = 2 * n
    assert d1.topython() == [[None] * nn + [False] * nn + [True] * nn]


@pytest.mark.parametrize("n", [254, 255, 256, 257, 258, 1000, 10000])
def test_i1b_large_stable(n):
    d0 = datatable.DataTable([[True, False, None] * n, list(range(3 * n))],
                             colnames=["A", "B"])
    assert d0.stypes[0] == "i1b"
    d1 = d0(sort="A", select="B")
    assert d1.internal.isview
    assert d1.internal.check()
    assert d1.topython() == [list(range(2, 3 * n, 3)) +
                             list(range(1, 3 * n, 3)) +
                             list(range(0, 3 * n, 3))]



#-------------------------------------------------------------------------------

def test_i2i_small():
    d0 = datatable.DataTable([0, -10, 100, -1000, 10000, 2, 999, None])
    assert d0.stypes[0] == "i2i"
    d1 = d0(sort=0)
    assert d1.internal.check()
    assert d1.topython() == [[None, -1000, -10, 0, 2, 100, 999, 10000]]


def test_i2i_small_stable():
    d0 = datatable.DataTable([[0, 1000, 0, 0, 1000, 0, 0, 1000, 0],
                              [1, 2, 3, 4, 5, 6, 7, 8, 9]])
    assert d0.stypes[0] == "i2i"
    d1 = d0(sort=0)
    assert d1.internal.check()
    assert d1.topython() == [[0, 0, 0, 0, 0, 0, 1000, 1000, 1000],
                             [1, 3, 4, 6, 7, 9, 2, 5, 8]]


def test_i2i_large():
    d0 = datatable.DataTable([(i * 111119) % 10007 - 5003
                              for i in range(10007)])
    d1 = d0(sort=0)
    assert d1.stypes == ("i2i", )
    assert d1.internal.check()
    assert d1.topython() == [list(range(-5003, 5004))]


@pytest.mark.parametrize("n", [100, 150, 200, 500, 1000, 200000])
def test_i2i_large_stable(n):
    d0 = datatable.DataTable([[-5, None, 5, -999, 1000] * n,
                              list(range(n * 5))], colnames=["A", "B"])
    assert d0.stypes[0] == "i2i"
    d1 = d0(sort="A", select="B")
    assert d1.internal.check()
    assert d1.topython() == [list(range(1, 5 * n, 5)) +
                             list(range(3, 5 * n, 5)) +
                             list(range(0, 5 * n, 5)) +
                             list(range(2, 5 * n, 5)) +
                             list(range(4, 5 * n, 5))]



#-------------------------------------------------------------------------------

def test_i8i_small():
    d0 = datatable.DataTable([10**(i * 101 % 13) for i in range(13)] + [None])
    assert d0.stypes == ("i8i", )
    d1 = d0(sort=0)
    assert d1.stypes == d0.stypes
    assert d1.internal.check()
    assert d1.topython() == [[None] + [10**i for i in range(13)]]


def test_i8i_small_stable():
    d0 = datatable.DataTable([[0, None, -1000, 11**11] * 3, list(range(12))])
    assert d0.stypes == ("i8i", "i1i")
    d1 = d0(sort=0, select=1)
    assert d1.internal.check()
    assert d1.topython() == [[1, 5, 9, 2, 6, 10, 0, 4, 8, 3, 7, 11]]


@pytest.mark.parametrize("n", [16, 20, 30, 40, 50, 100, 500, 1000])
def test_i8i_large0(n):
    a = -6654966461866573261
    b = -6655043958000990616
    c = 5207085498673612884
    d = 5206891724645893889
    d0 = datatable.DataTable([c, d, a, b] * n)
    d1 = d0(sort=0)
    assert d0.internal.check()
    assert d1.internal.check()
    assert d1.internal.isview
    assert b < a < d < c
    assert d0.topython() == [[c, d, a, b] * n]
    assert d1.topython() == [[b] * n + [a] * n + [d] * n + [c] * n]


@pytest.mark.parametrize("seed", [random.getrandbits(63) for i in range(10)])
def test_i8i_large_random(seed):
    random.seed(seed)
    m = 2**63 - 1
    tbl = [random.randint(-m, m) for i in range(1000)]
    d0 = datatable.DataTable(tbl)
    assert d0.stypes == ("i8i", )
    d1 = d0(sort=0)
    assert d1.topython() == [sorted(tbl)]