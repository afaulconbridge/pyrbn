PyRBN
=====

A python library for Random Boolean Networks.

Designed to be simple and fast, works particularly well with PyPy.


Development
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

Run tests with:

```sh
pytest
```

Test coverage with:

```sh
coverage run --source=pyrbn -m pytest
coverage report -m
```

TODO
----

performance comparison of backends
 - [networkx](https://networkx.github.io/documentation/stable/)
 - [python-igraph](https://igraph.org/python/)
 - [graph-tool](https://graph-tool.skewed.de/)
 - [numpy](https://susan-stepney.blogspot.com/2013/01/rbns-with-numpy-sorted.html)
   - done, slower than pure python or pypy
