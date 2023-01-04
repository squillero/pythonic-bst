# PYTHONIC BST

A minimalistic, unbalanced Binary Search Tree written in pure Python.

The `bst` works almost like a `dict`, but keys are kept sorted and slicing is partially supported. The methods exploit *lazy execution* when possible, all relevant operations are $O(log)$ complexity.

## BASIC USAGE

```python
from bst import BST
```

* Create an empty BST: `mybst = BST()`
* Duplicate a BST: `mybst2 = BST(mybst)`
* Convert from/to a dict:`mybst = BST(mydict)` / `mydict = dict(mybst)`
* Create a BST from a sequence of $(k, v)$ pairs: `mybst = BST([(18, 5), (23, 10)])`
* Add/update an item: `mybst[k] = v`
* Remove an existing item: `rm mybst[k]`
* Count items: `len(mybst)`
* Check wether a key is present: `if k in mybst: ...`
* Check if the BST is not empty: `if mybst: ...`
* Iterate forward: `for k, v in mybst: ...`
* Iterate backward: `for k, v in reversed(mybst): ...`
* Iterate forward on keys $k \in [k_1, k_2[$: `for k, v in mybst[k1:k2]: ...`
* Iterate backward on keys $k \in ]k_1, k_2]$: `for k, v in mybst[k2:k1:-1]: ...`
* Generate all the keys: `mybst.keys()`
* Generate all the values: `mybst.values()`
* Generate all $(k, v)$ pairs: `mybst.items()`
* Standard BST-esque visits: `mybst.visit_in_order()`, `mybst.visit_pre_order()`, `mybst.visit_post_order()`

## PERFORMANCES

The *density* (percentage of internal nodes that have two successors) and the *unbalance* (relative difference between the longest and the shortest path from the root) may be accessed as properties, although at a **significant** cost:

```python
mybst = BST()
for n in range(1_000_000):
    mybst[random.random()] = n
mybst.density, mybst.unbalance
```

may yield something like

```python
(0.5007653911148597, 0.86)
```

Initializing a BST from known data would create an almost optimized data structure:

```python
mybst2 = BST(mybst)
mybst2.density, mybst2.unbalance
```

may yield something like

```python
(0.9073503634459752, 0.05)
```

**Copyright © 2022 by Giovanni Squillero**  
Distributed under a [Zero-Clause BSD License](https://tldrlegal.com/license/bsd-0-clause-license) (SPDX: [0BSD](https://spdx.org/licenses/0BSD.html)), which allows unlimited freedom with the software without the requirement to include legal notices. See the full [license file](./LICENSE.md) for details.
