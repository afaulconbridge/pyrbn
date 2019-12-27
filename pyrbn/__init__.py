import itertools
from typing import Dict, List, Tuple


class RBN:
    states: Tuple[bool] = ()
    inputs: Tuple[Tuple[int]] = ()
    funcs: Tuple[Dict[Tuple[bool], bool]] = ()

    def __init__(
        self,
        states: Tuple[bool],
        inputs: Tuple[int],
        funcs: Tuple[Dict[Tuple[bool], bool]],
    ):
        self.n = len(states)
        assert self.n == len(inputs)
        assert self.n > 0
        self.k = len(inputs[0])
        assert self.k == max((len(i) for i in inputs))
        assert self.k == min((len(i) for i in inputs))
        assert self.n == len(funcs)
        assert self.n > max(itertools.chain(*inputs))
        assert 0 >= min(itertools.chain(*inputs))
        self.states = tuple(states)
        self.inputs = tuple(inputs)
        self.funcs = funcs

    @classmethod
    def from_random(clzz, rng, n=5, k=2):
        states = [rng.random() >= 0.5 for i in range(n)]
        inputs = tuple(zip(*(list(rng.sample(range(n), n)) for i in range(k))))
        funcs = []
        keys = tuple(itertools.product((True, False), repeat=2))
        for i in range(n):
            func = {}
            for key in keys:
                value = rng.random() >= 0.5
                func[tuple(key)] = value
            funcs.append(func)

        return clzz(states, inputs, funcs)

    def __repr__(self):
        return "{}({}, {}, {})".format(
            type(self).__name__, self.states, self.inputs, self.funcs
        )

    def next_state(self, state=None):
        if state is None:
            state = self.states
        return tuple(
            [
                self.funcs[i][tuple((state[self.inputs[i][j]] for j in range(self.k)))]
                for i in range(self.n)
            ]
        )

    def find_cycle(self, state=None):
        if state is None:
            state = self.states
        current_state = state
        next_state = self.next_state(current_state)
        seen = {current_state: next_state}
        while next_state not in seen:
            seen[current_state] = next_state
            current_state = next_state
            next_state = self.next_state(current_state)

        return seen
