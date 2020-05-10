import itertools
from typing import Dict, List, Tuple

import numpy as np

from .basic import RBNBasic


"""
This seems to actually be slower than pure python for some reason?
based on https://susan-stepney.blogspot.com/2013/01/rbns-with-numpy-sorted.html
"""


class RBNNumpy(RBNBasic):
    funcs_fast = None
    pows = []

    def __init__(self, states: Tuple[bool], inputs: Tuple[int], funcs: Tuple[Dict[Tuple[bool], bool]]):
        super(RBNNumpy, self).__init__(states, inputs, funcs)

        # pre compute powers of two
        if self.k > len(self.pows):
            RBNNumpy.pows = 2 ** np.arange(self.k)

        # convert funcs into a 2D array for quicker lookup
        # note this assumes funcs keys is in sorted order
        self.funcs_fast = np.array([[f[key] for key in f.keys()] for f in funcs], np.int32)

        self.inputs = np.array(self.inputs, np.int32)
        self.states = np.array(self.states, np.int32)  # use an int so we can multiply later

    def next_state(self, state=None):
        if state is None:
            state = self.states
        return self.funcs_fast[:, np.sum(self.pows * state[self.inputs], 1)].diagonal()
