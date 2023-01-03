# PYTHONIC BST

A minimalistic, unbalanced Binary Search Tree written in pure Python.

The `bst` works almost like a `dict`, but keys are kept sorted and slicing is partially supported.The methods exploit *lazy execution* when possible, all relevant operations are $O(log)$ complexity.

## BASIC USAGE

```python
from bst import BST
foo = BST()
```

* Add/update an element: `foo[k] = v`
* Remove an existing element: `rm foo[k]`
* Count elements: `len(foo)`
* Check wether a key is present: `if k in foo: ...`
* Check if the BST is not empty: `if foo: ...`
* Iterate forward: `for k, v in foo: ...`
* Iterate backward: `for k, v in reversed(foo): ...`
* Iterate forward on keys $k \in [k_1, k_2[$: `for k, v in foo[k1:k2]: ...`
* Iterate backward on keys $k \in ]k_1, k_2]$: `for k, v in foo[k2:k1:-1]: ...`
* Get a list with all the keys: `foo.keys()`
* Get a list with all the values: `foo.values()`
* Get a list with all (key, value) pairs: `foo.items()`
* Standard BST-esque visits: `foo.visit_in_order()`, `foo.visit_pre_order()`, `foo.visit_post_order()`

**Copyright © 2022 by Giovanni Squillero**  
Distributed under a *Free Public License* (also known as [*Zero-Clause BSD*](https://tldrlegal.com/license/bsd-0-clause-license)): anyone is free to use, copy, and modify this software for any
purpose.
