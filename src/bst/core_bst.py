# ___  _   _ ___ _  _ ____ _  _ _ ____    ___  ____ ___
# |__]  \_/   |  |__| |  | |\ | | |       |__] [__   |
# |      |    |  |  | |__| | \| | |___    |__] ___]  |
# <=<=<<https://github.com/squillero/pythonic-bst>>=>=>

# Copyright 2022 Giovanni Squillero.
# SPDX-License-Identifier: 0BSD

import logging


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

    def __le__(self, other):
        return self._key <= other._key


class BST:
    """A minimalistic, unbalanced Binary Search Tree written in pure Python.

    The `bst` works almost like a `dict`, but keys are kept sorted and slicing is partially supported.

    Exploit lazy execution when possible, all relevant operations are O(log) complexity.


    """

    def __init__(self):
        self._root = None
        self._min_node = None
        self._max_node = None
        self._num_nodes = 0

    def add(self, key, value):
        """Add a node in the BST. Keys must be mutually comparable."""

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

    def _get_min(self):
        """Get node with minimum key"""
        node = self._root
        if node is None:
            return None
        while node.left:
            node = node.left
        return node

    def _get_max(self):
        """Get node with maximum key"""
        node = self._root
        if node is None:
            return None
        while node.right:
            node = node.right
        logging.debug(f"MAX: {node}")
        return node

    def delete(self, key):
        """Delete the pair (key, value) from the BST."""
        node = self._find_node(key, croak=True)
        update_min = node == self._min_node
        update_max = node == self._max_node

        self._delete(node)
        if update_max:
            self._max_node = self._get_max()
        if update_min:
            self._min_node = self._get_min()
        self._num_nodes -= 1

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

    def __contains__(self, key):
        """Standard customizaton: in"""
        return self._find_node(key) is not None

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

    def keys(self):
        return (k for k, _ in self._node_iterator())

    def values(self):
        return (v for _, v in self._node_iterator())

    def items(self):
        return self._node_iterator()

    def __iter__(self):
        """Standard customizaton (forward iterator)"""
        return self._node_iterator()

    def __reversed__(self):
        """Standard customizaton (reverse iterator)"""
        return self._node_reverse_iterator()

    def __getitem__(self, key):
        """Standard customizaton"""
        if isinstance(key, slice):
            if key.step is None or key.step == 1:
                return self._node_iterator(key.start, key.stop)
            elif key.step == -1:
                return self._node_reverse_iterator(key.start, key.stop)
            else:
                assert abs(key.step) != 1, "Only +/-1 steps are supported in slicing"
        else:
            node = self._find_node(key, croak=True)
            if node is not None:
                return node.value
            else:
                return None

    def __setitem__(self, key, value):
        """Standard customizaton"""
        self.add(key, value)

    def __delitem__(self, key):
        """Standard customizaton"""
        self.delete(key)

    def __len__(self):
        """Standard customizaton"""
        return self._num_nodes
