from typing import List, Tuple

import cachetools

from .basic import RBNBasic


class RBNSorted(RBNBasic):
    def __init__(
        self, states: Tuple[bool], inputs: Tuple[int], funcs: Tuple[Tuple[bool]]
    ):
        # sort the inputs and update accordingly
        node_mapping = [
            x[0] for x in sorted(enumerate(zip(funcs, inputs)), key=lambda x: x[1])
        ]
        funcs = tuple((funcs[i] for i in node_mapping))
        inputs = tuple((tuple((node_mapping[i] for i in inputk)) for inputk in inputs))
        # sort twice to ensure inputs are ordered correctly too
        node_mapping = [
            x[0] for x in sorted(enumerate(zip(funcs, inputs)), key=lambda x: x[1])
        ]
        funcs = tuple((funcs[i] for i in node_mapping))
        inputs = tuple((tuple((node_mapping[i] for i in inputk)) for inputk in inputs))

        super(RBNSorted, self).__init__(states, inputs, funcs)
