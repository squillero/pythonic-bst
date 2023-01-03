# ___  _   _ ___ _  _ ____ _  _ _ ____    ___  ____ ___
# |__]  \_/   |  |__| |  | |\ | | |       |__] [__   |
# |      |    |  |  | |__| | \| | |___    |__] ___]  |
# <=<=<<https://github.com/squillero/pythonic-bst>>=>=>

# Copyright 2022 Giovanni Squillero.
# SPDX-License-Identifier: 0BSD

import logging
import random
from bst import BST


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
