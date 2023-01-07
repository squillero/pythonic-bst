# ___  _   _ ___ _  _ ____ _  _ _ ____    ___  ____ ___
# |__]  \_/   |  |__| |  | |\ | | |       |__] [__   |
# |      |    |  |  | |__| | \| | |___    |__] ___]  |
# <=<=<<https://github.com/squillero/pythonic-bst>>=>=>

# Copyright 2022 Giovanni Squillero.
# SPDX-License-Identifier: 0BSD

import logging
from math import nan
from collections import defaultdict


class _Node:
    """BST node (internal)"""

    def __init__(self, key, value):
        self._key = key
        self._value = value
        self._parent = None
        self._right = None
        self._left = None

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    @property
    def parent(self):
        return self._parent

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, new_value):
        self._left = new_value
        if new_value:
            new_value._parent = self

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, new_value):
        self._right = new_value
        if new_value:
            new_value._parent = self

    @staticmethod
    def n2s(node):
        if node is None:
            return repr(None)
        else:
            return f"({node._key!r}:{node._value!r})"

    def __iter__(self):
        return (i for i in [self._key, self._value])

    def __str__(self):
        return f"{_Node.n2s(self)} <{_Node.n2s(self.left)} ^{_Node.n2s(self.parent)} >{_Node.n2s(self.right)}"

    def __eq__(self, other):
        return other is not None and self._key == other._key

    def __lt__(self, other):
        return self._key < other._key


class BST:
    """A minimalistic, unbalanced Binary Search Tree written in pure Python.

    The class `BST` works almost like a `dict` with sorted keys, and supports slicing and broadcasting.\\
    The methods exploit lazy execution when possible, all relevant operations are O(log) complexity.
    """

    def __init__(self, init=None):
        self._root = None
        self._min_node = None
        self._max_node = None
        self._num_nodes = 0
        if isinstance(init, dict):
            init = init.items()
        if init is not None:
            order = list()
            elements = sorted(list(init))
            BST._order_list(elements, 0, len(elements), order)
            for k, v in order:
                self.set(k, v)

    @property
    def height(self):
        if self._num_nodes == 0:
            return 0
        elif self._num_nodes == 1:
            return 1
        pl = defaultdict(int)
        pl[self._root.key] = 0
        BST._update_path_length(self._root, pl)
        return 1 + max(pl.values())

    @property
    def density(self):
        if not self._root:
            return nan
        os = defaultdict(int)
        BST._update_offspring_size(self._root, os)
        if not sum(o > 0 for o in os.values()):
            return nan
        return 1 - sum(o == 1 for o in os.values()) / sum(o > 0 for o in os.values())

    @property
    def unbalance(self):
        if self._num_nodes < 1:
            return nan
        os = defaultdict(int)
        BST._update_offspring_size(self._root, os)
        pl = defaultdict(int)
        pl[self._root.key] = 0
        BST._update_path_length(self._root, pl)
        paths = [p for k, p in pl.items() if os[k] < 2]
        return (max(paths) - min(paths)) / (1 + max(paths))

    @staticmethod
    def _order_list(seq, start, end, solution):
        if start >= end:
            return
        m = start + (end - start) // 2
        solution.append(seq[m])
        BST._order_list(seq, start, m, solution)
        BST._order_list(seq, m + 1, end, solution)

    @staticmethod
    def _visit(node, pre_order=None, in_order=None, post_order=None):
        """Generic recursive visit in pre-/in-/post- order"""
        assert sum([pre_order is not None, in_order is not None, post_order
                    is not None]) == 1, f"Exactly one type of visit must be specified."
        if node is not None:
            if pre_order is not None:
                pre_order.append((node.key, node.value))
                BST._visit(node.left, pre_order, in_order, post_order)
                BST._visit(node.right, pre_order, in_order, post_order)
            if in_order is not None:
                BST._visit(node.left, pre_order, in_order, post_order)
                in_order.append((node.key, node.value))
                BST._visit(node.right, pre_order, in_order, post_order)
            if post_order is not None:
                BST._visit(node.left, pre_order, in_order, post_order)
                BST._visit(node.right, pre_order, in_order, post_order)
                post_order.append((node.key, node.value))

    @staticmethod
    def _update_offspring_size(node, size):
        size[node.key] += 0
        if node.left:
            size[node.key] += 1
            BST._update_offspring_size(node.left, size)
        if node.right:
            size[node.key] += 1
            BST._update_offspring_size(node.right, size)

    @staticmethod
    def _update_path_length(node, path_len):
        if node.left:
            path_len[node.left.key] = path_len[node.key] + 1
            BST._update_path_length(node.left, path_len)
        if node.right:
            path_len[node.right.key] = path_len[node.key] + 1
            BST._update_path_length(node.right, path_len)

    def _find_min(self):
        """Get node with minimum key"""
        node = self._root
        if node is None:
            return None
        while node.left:
            node = node.left
        return node

    def _find_max(self):
        """Get node with maximum key"""
        node = self._root
        if node is None:
            return None
        while node.right:
            node = node.right
        logging.debug(f"MAX: {node}")
        return node

    def _replace_node(self, old_node, new_node):
        """Replace old_node with new_node in old_node's parent."""
        if not old_node.parent:
            self._root = new_node
            new_node._parent = None
        elif old_node.parent.right == old_node:
            old_node.parent.right = new_node
        else:
            old_node.parent.left = new_node

    def _delete(self, node):
        """Remove node from BST."""
        if not node.left and not node.right:
            if node.parent:
                self._replace_node(node, None)
            else:
                self._root = None
        elif not node.left:
            self._replace_node(node, node.right)
        elif not node.right:
            self._replace_node(node, node.left)
        else:
            successor = self._successor(node)
            k, v = successor.key, successor.value
            self._delete(successor)
            node._key, node._value = k, v

    def _find_node(self, key, croak=False):
        """Return the node with the given key, None if not present unless croaking"""
        node = self._root
        while node is not None and node.key != key:
            if key > node.key:
                node = node.right
            elif key < node.key:
                node = node.left
        if croak and node is None:
            raise KeyError(key)
        else:
            return node

    def _slice2iter(self, slice_):
        if slice_.step is None or slice_.step == 1:
            return self._node_iterator(slice_.start, slice_.stop)
        elif slice_.step == -1:
            return self._node_reverse_iterator(slice_.start, slice_.stop)
        else:
            raise ValueError("Only +/-1 steps are supported in slicing")

    def _successor(self, node):
        """Return the next node as in a in-order visit"""
        if node.right is not None:
            # one step right, then a good run on the left
            node = node.right
            while node.left is not None:
                node = node.left
        else:
            # up/left while possible
            while node.parent is not None and node.parent.right == node:
                node = node.parent
            node = node.parent
        return node

    def _predecessor(self, node):
        """Return the previous node as in a in-order visit"""
        if node.left is not None:
            # one step left, then a good run on the right
            node = node.left
            while node.right is not None:
                node = node.right
        else:
            # up/right while possible
            while node.parent is not None and node.parent.left == node:
                node = node.parent
            node = node.parent
        return node

    def _node_iterator(self, start_key=None, stop_key=None):
        """Iterator on nodes using successor(n)."""
        if start_key is not None:
            node = self._find_node(start_key, croak=True)
        else:
            node = self._min_node
        while node and (stop_key is None or node.key < stop_key):
            yield (node.key, node.value)
            node = self._successor(node)

    def _node_reverse_iterator(self, start_key=None, stop_key=None):
        """Iterator on nodes using successor(n)."""
        if start_key is not None:
            node = self._find_node(start_key, croak=True)
        else:
            node = self._max_node
        while node and (stop_key is None or node.key > stop_key):
            yield (node.key, node.value)
            node = self._predecessor(node)

    def set(self, key, value):
        """Add a node in the BST. Note: Keys must be comparable."""

        new_node = _Node(key, value)
        last_node = None
        current_node = self._root
        while current_node is not None:
            last_node = current_node
            if new_node == current_node:
                current_node.value = value
                break
            elif new_node > current_node:
                current_node = current_node.right
            elif new_node < current_node:
                current_node = current_node.left
        else:
            self._num_nodes += 1
            if last_node is None:
                self._min_node = new_node
                self._max_node = new_node
                self._root = new_node
            elif new_node > last_node:
                if new_node > self._max_node:
                    self._max_node = new_node
                last_node.right = new_node
            else:
                if new_node < self._min_node:
                    self._min_node = new_node
                last_node.left = new_node

    def delete(self, key):
        """Delete the pair (key, value) from the BST."""
        node = self._find_node(key, croak=True)
        update_min = node == self._min_node
        update_max = node == self._max_node

        self._delete(node)
        if update_max:
            self._max_node = self._find_max()
        if update_min:
            self._min_node = self._find_min()
        self._num_nodes -= 1

    def visit_in_order(self):
        """Returns all the (key, value) pairs through an in-order visit"""
        ret = list()
        BST._visit(self._root, in_order=ret)
        return ret

    def visit_pre_order(self):
        """Returns all the (key, value) pairs through an pre-order visit"""
        ret = list()
        BST._visit(self._root, pre_order=ret)
        return ret

    def visit_post_order(self):
        """Returns all the (key, value) pairs through a post-order visit"""
        ret = list()
        BST._visit(self._root, post_order=ret)
        return ret

    def keys(self):
        return (k for k, _ in self._node_iterator())

    def values(self):
        return (v for _, v in self._node_iterator())

    def items(self):
        return self._node_iterator()

    def __len__(self):
        """Standard customizaton: len(bst)"""
        return self._num_nodes

    def __eq__(self, other):
        """Standard customizaton: =="""
        return len(self) == len(other) and all(n1 == n2 for n1, n2 in zip(self, other))

    def __contains__(self, key):
        """Standard customizaton: k in bst"""
        return self._find_node(key) is not None

    def __iter__(self):
        """Standard customizaton (forward iterator)"""
        return self._node_iterator()

    def __reversed__(self):
        """Standard customizaton (reverse iterator)"""
        return self._node_reverse_iterator()

    def __getitem__(self, key):
        """Standard customizaton"""
        if isinstance(key, slice):
            return self._slice2iter(key)
        else:
            return self._find_node(key, croak=True).value

    def __setitem__(self, key, value):
        """Standard customizaton: bst[*] = *"""
        if not isinstance(key, slice):
            self.set(key, value)
        else:
            keys = list(k for k, _ in self._slice2iter(key))
            try:
                values = list(value)
            except TypeError:
                values = [value] * len(keys)
            for k, v in zip(keys, values):
                self.set(k, v)

    def __delitem__(self, key):
        """Standard customizaton: bst[k]"""
        if not isinstance(key, slice):
            self.delete(key)
        else:
            for k in list(k for k, _ in self._slice2iter(key)):
                self.delete(k)
