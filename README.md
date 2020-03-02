TODO
====


development
-----------

Install using pip including development extras

```sh
pip install -e .[dev]
```

Enable pre-commit hooks with:

```sh
pre-commit install
```

Freeze dependencies with:

```sh
pip-compile
```

TODO
----

implement backends with
 - [networkx](https://networkx.github.io/documentation/stable/)
 - [python-igraph](https://igraph.org/python/)
 - [graph-tool](https://graph-tool.skewed.de/)
 - [numpy](https://susan-stepney.blogspot.com/2013/01/rbns-with-numpy-sorted.html)

performance comparison of backends
