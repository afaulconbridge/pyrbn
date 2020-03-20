from typing import Iterable

from .basic import RBNBasic


class RBNSorted(RBNBasic):
    def __init__(
        self,
        states: Iterable[bool],
        inputs: Iterable[int],
        funcs: Iterable[Iterable[bool]],
    ):

        # swap functions if necessary
        funcs = tuple(funcs)
        inputs = list(inputs)
        for i in range(len(funcs)):
            # 00 0
            # 01 1 } swap if { True
            # 10 2 }         { False
            # 11 3

            if funcs[i][1] and not funcs[i][2]:
                funcs[i][1] = False
                funcs[i][2] = True

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
