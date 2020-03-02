import itertools
from typing import Dict, List, Tuple

from .basic import RBNBasic


class RBNFast(RBNBasic):
    funcs_fast = None
    pows = []

    def __init__(
        self,
        states: Tuple[bool],
        inputs: Tuple[int],
        funcs: Tuple[Dict[Tuple[bool], bool]],
    ):
        super(RBNFast, self).__init__(states, inputs, funcs)

        # pre compute powers of two
        while self.k >= len(self.pows):
            self.pows.append(2 ** (len(self.pows)))

        # convert funcs into a 2D array for quicker lookup
        # note this assumes funcs keys is in sorted order
        self.funcs_fast = [[f[key] for key in f.keys()] for f in funcs]

    def next_state(self, state=None):
        if state is None:
            state = self.states
        return [
            self.funcs_fast[i][
                sum((self.pows[j] for j in range(self.k) if state[self.inputs[i][j]]))
            ]
            for i in range(self.n)
        ]
