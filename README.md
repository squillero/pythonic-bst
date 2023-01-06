# PYTHONIC BST

A minimalistic, unbalanced Binary Search Tree written in pure Python.

The `BST` works almost like a `dict` with sorted keys, supporting slicing and broadcasting. The methods exploit *lazy execution* when possible, all relevant operations are $O(log)$ complexity.

## NOTES

Keys must be comparable.

All `slice`s are half-open. That is, `[k1:k2]` specifies keys $k_1 \le k < k_2$; while `[k2:k1:-1]` specifies keys $k_1 \ge k > k_2$ in reverse arder. Key `k1` must be present in the BST, key `k2` is never included.

## BASIC USAGE

```python
from bst import BST
```

* Create an empty BST: `foo = BST()`
* Add/update an item: `foo[k] = v`
* Remove an existing item: `rm foo[k]`
* Count items: `len(foo)`
* Check wether key $k$ is present: `if k in foo: ...`
* Check if the BST is not empty: `if foo: ...`
* Iterate forward: `for k, v in foo: ...`
* Iterate backward: `for k, v in reversed(foo): ...`
* Generate all the keys: `foo.keys()`
* Generate all the values: `foo.values()`
* Generate all $(k, v)$ pairs: `foo.items()`
* Standard BST-esque visits: `foo.visit_in_order()`, `foo.visit_pre_order()`, `foo.visit_post_order()`

## INITIALIZATION / CONVERSION

A BST can be initialized from a sequence of $(k, v)$ pairs, like another BST's iterator.

* Duplicate a BST: `bar = BST(foo)`
* Initialize a BST from a generic sequence of pairs: `foo = BST([(18, 5), (23, 10)])`

A dictionary may be used directly to initialize a BST and vice-versa.

* Initialize from a dictionary: `foo = BST(baz)`
* Create a dictionary from a BST: `baz = dict(foo)`

## SLICING / BROADCASTING

* Iterate forward on keys $k \in [k_1, k_2[$: `for k, v in foo[k1:k2]: ...`
* Iterate backward on keys $k \in ]k_1, k_2]$: `for k, v in foo[k2:k1:-1]: ...`

* Update the first three items with keys $k \in [k_1, k_2[$: `foo[k1:k2] = [v1, v2, v3]`
* Set all items with keys $k < k_2$ to a specific value: `foo[:k2] = v`
* Remove item with key $k_1$ and all subsequent ones: `rm foo[k1:]`

## PERFORMANCES

The *height* (longest path from the root), the *density* (percentage of internal nodes that have two successors), and the *unbalance* (relative difference between the longest and the shortest path from the root) may be accessed as properties, although at a **significant** cost.

```python
foo = BST()
for n in range(1_000_000):
    foo[random.random()] = n
print(foo.height, foo.density, foo.unbalance)

# Initializing from known data creates an optimized structure
bar = BST(foo)
print(bar.height, bar.density, bar.unbalance)
```

may yield something like

```python
49 0.4997143041393656 0.8775510204081632
20 0.9073503634459752 0.05
```

**Copyright © 2022 by Giovanni Squillero**  
Distributed under a [Zero-Clause BSD License](https://tldrlegal.com/license/bsd-0-clause-license) (SPDX: [0BSD](https://spdx.org/licenses/0BSD.html)), which allows unlimited freedom with the software without the requirement to include legal notices. See the full [license file](./LICENSE.md) for details.
