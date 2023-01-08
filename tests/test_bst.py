# ___  _   _ ___ _  _ ____ _  _ _ ____    ___  ____ ___
# |__]  \_/   |  |__| |  | |\ | | |       |__] [__   |
# |      |    |  |  | |__| | \| | |___    |__] ___]  |
# <=<=<<https://github.com/squillero/pythonic-bst>>=>=>

# Copyright 2023 Giovanni Squillero.
# SPDX-License-Identifier: 0BSD

import logging
import random
from math import nan
import pytest

from bst import BST


def create_random_bst(size):
    bst = BST()
    for n in range(size):
        bst[random.random() * 2 - 1] = n + 1
    bst[0] = 0
    return bst


def test_iter():
    bst = create_random_bst(1000)
    assert set(bst[::]) == set(bst[::-1])
    assert set(iter(bst)) == set(reversed(bst))


def test_add_remove_base():
    random.seed(42)
    for rep in range(2):
        bst = BST()
        d = dict()
        for n in range(100):
            bst[n] = n
            d[n] = n
            set(bst.keys()) == set(d.keys())
            assert len(bst) == len(d)
            assert len(bst) == 0 or bst._min_node.key == min(bst.keys())
            assert len(bst) == 0 or bst._max_node.key == max(bst.keys())
        removed = set()

        while bst:
            logging.debug(f"")
            set(bst.keys()) == set(d.keys())
            set(bst.values()) == set(d.values())
            elem = random.choice(list(bst.keys()))
            removed.add(elem)
            assert elem in bst, f"{removed}"
            assert elem in d, f"{removed}"
            logging.debug(f"MIN: {bst._min_node.key} // MAX: {bst._max_node.key}")
            assert len(bst) == 0 or bst._min_node.key == min(bst.keys())
            assert len(bst) == 0 or bst._max_node.key == max(bst.keys())
            del d[elem]
            assert elem not in d
            del bst[elem]
            with pytest.raises(KeyError):
                print(bst[elem])
            assert elem not in bst, f"{elem} still in {list(bst)}"
            assert len(bst) == 0 or bst._min_node.key == min(bst.keys())
            assert len(bst) == 0 or bst._max_node.key == max(bst.keys())


def test_add_remove_ext():
    for loop in range(42):
        x = BST()
        y = dict()

        for elem in range(100):
            k = round(1_000 * random.random())
            v = int(k * 1_000_000)
            x[k] = v
            y[k] = v
            assert len(x) == len(y)
            assert list(x.keys()) == sorted(y.keys())
            assert tuple(x._min_node) == min(x.items())
            assert tuple(x._max_node) == max(x.items())

        while x and y:
            k = random.choice(list(y.keys()))
            assert len(x) == len(y)
            assert list(x.keys()) == sorted(y.keys())
            assert x[k] == y[k]
            assert tuple(x._min_node) == min(x.items())
            assert tuple(x._max_node) == max(x.items())
            del x[k]
            del y[k]
            assert len(x) == 0 or tuple(x._min_node) == min(x.items())
            assert len(x) == 0 or tuple(x._max_node) == max(x.items())
            assert len(x) == len(y)
            assert list(x.keys()) == sorted(y.keys())


def test_slice():
    for loop in range(42):
        refs = [(n, n) for n in list(range(1000))]
        bst = BST()
        keys = list(range(1000))
        random.shuffle(keys)
        for k in keys:
            bst[k] = k
        for rep in range(100):
            a, b = random.randint(0, 1000 - 1), random.randint(0, 1000 - 1)
            assert list(bst[a:b]) == list(refs[a:b])
            assert list(bst[a:b:-1]) == list(refs[a:b:-1])
        bst[10:100] = list(range(90))
        bst[10:50] = None


def test_slice_exception():
    bst = BST((n, n) for n in range(10))
    del bst[::]
    bst = BST((n, n) for n in range(10))
    del bst[::1]
    bst = BST((n, n) for n in range(10))
    del bst[::-1]
    with pytest.raises(ValueError) as exc_info:
        bst = BST((n, n) for n in range(10))
        del bst[::2]
    with pytest.raises(ValueError) as exc_info:
        bst = BST((n, n) for n in range(10))
        del bst[::-2]


def test_init():
    bst = create_random_bst(1_000)

    list_ = list(bst)
    list2_ = list(bst.items())
    assert list_ == list2_

    dict_ = dict(bst)
    dict2_ = dict(bst.items())
    assert dict_ == dict2_

    bst_l = BST(list_)
    bst_d = BST(dict_)
    assert bst_l == bst
    assert bst_d == bst


def test_performances():
    bst = BST()
    assert (bst.height, bst.density, bst.unbalance) == (0, nan, nan)
    bst[23] = 10
    assert (bst.height, bst.density, bst.unbalance) == (1, nan, 0.0)
    bst[18] = 5
    assert (bst.height, bst.density, bst.unbalance) == (2, 0.0, 0.5)
    for n in range(-20, 20, 1):
        bst[n] = n
    assert (bst.height, bst.density, bst.unbalance) == (40, 0.02564102564102566, 0.975)


def test_visit():
    bst = BST([n, n] for n in range(-5, 6))
    assert bst.visit_in_order() == [(n, n) for n in range(-5, 6)]
    assert bst.visit_post_order() == [(-5, -5), (-4, -4), (-2, -2), (-1, -1), (-3, -3), (1, 1),
                                      (2, 2), (4, 4), (5, 5), (3, 3), (0, 0)]
    assert bst.visit_pre_order() == [(0, 0), (-3, -3), (-4, -4), (-5, -5), (-1, -1), (-2, -2),
                                     (3, 3), (2, 2), (1, 1), (5, 5), (4, 4)]
