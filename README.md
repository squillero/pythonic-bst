# PYTHONIC BST

A minimalistic, unbalanced Binary Search Tree written in pure Python.

The `bst` works almost like a `dict`, but keys are kept sorted and slicing is partially supported. The methods exploit *lazy execution* when possible, all relevant operations are $O(log)$ complexity.

## BASIC USAGE

```python
from bst import BST
```

* Create an empty BST: `foo = BST()`
* Duplicate a BST: `bar = BST(foo)`
* Convert from/to a dict:`foo = BST(mydict)` / `mydict = dict(foo)`
* Create a BST from a sequence of $(k, v)$ pairs: `foo = BST([(18, 5), (23, 10)])`
* Add/update an item: `foo[k] = v`
* Remove an existing item: `rm foo[k]`
* Count items: `len(foo)`
* Check wether a key is present: `if k in foo: ...`
* Check if the BST is not empty: `if foo: ...`
* Iterate forward: `for k, v in foo: ...`
* Iterate backward: `for k, v in reversed(foo): ...`
* Iterate forward on keys $k \in [k_1, k_2[$: `for k, v in foo[k1:k2]: ...`
* Iterate backward on keys $k \in ]k_1, k_2]$: `for k, v in foo[k2:k1:-1]: ...`
* Generate all the keys: `foo.keys()`
* Generate all the values: `foo.values()`
* Generate all $(k, v)$ pairs: `foo.items()`
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

```python
(0.5007653911148597, 0.86)
```

Initializing a BST from known data would create an almost optimized data structure:

```python
opt_bst = BST(bst)
opt_bst.density, opt_bst.unbalance
```

may yield something like

```python
(0.9073503634459752, 0.05)
```

**Copyright © 2022 by Giovanni Squillero**  
Distributed under a [Zero-Clause BSD License](https://tldrlegal.com/license/bsd-0-clause-license) (SPDX: [0BSD](https://spdx.org/licenses/0BSD.html)), which allows unlimited freedom with the software without the requirement to include legal notices. See the full [license file](./LICENSE.md) for details.
