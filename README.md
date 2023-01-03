# PYTHONIC BST

A minimalistic, unbalanced Binary Search Tree written in pure Python.

The `bst` works almost like a `dict`, but keys are kept sorted and slicing is partially supported. The methods exploit *lazy execution* when possible, all relevant operations are $O(log)$ complexity.

## BASIC USAGE

```python
from bst import BST
foo = BST()
```

* Add/update an element: `foo[k] = v`
* Remove an existing element: `rm foo[k]`
* Count elements: `len(foo)`
* Initialize from a dictionary or from any sequence of (key, value) pairs, including another BST: `foo = BST({23: 10, 18: 5})`
* Check wether a key is present: `if k in foo: ...`
* Check if the BST is not empty: `if foo: ...`
* Iterate forward: `for k, v in foo: ...`
* Iterate backward: `for k, v in reversed(foo): ...`
* Iterate forward on keys $k \in [k_1, k_2[$: `for k, v in foo[k1:k2]: ...`
* Iterate backward on keys $k \in ]k_1, k_2]$: `for k, v in foo[k2:k1:-1]: ...`
* Generate all the keys: `foo.keys()`
* Generate all the values: `foo.values()`
* Generate all (key, value) pairs: `foo.items()`
* Standard BST-esque visits: `foo.visit_in_order()`, `foo.visit_pre_order()`, `foo.visit_post_order()`

## PERFORMANCES

The *density* (percentage of internal nodes that have two successors) and the *unbalance* (relative difference between the longest and the shortest path from the root) may be accessed as properties, although at a **significant** cost:

```python
bst = BST()
for n in range(1_000_000):
    bst[random.random()] = n
bst.density, bst.unbalance
```

may yield something like

> `(0.5007653911148597, 0.86)`

Initializing a BST from a sequence of `(key, value)` pairs would create an almost optimized data structure:

```python
opt_bst = BST(bst)
opt_bst.density, opt_bst.unbalance
```

may yield something like

> `(0.9073503634459752, 0.05)`

**Copyright © 2022 by Giovanni Squillero**  
Distributed under the *Free Public License* (also known as [*Zero-Clause BSD*](https://tldrlegal.com/license/bsd-0-clause-license)), which allows unlimited freedom with the software without any requirement to include legal notices. See the [license file](./LICENSE.md) for details.
