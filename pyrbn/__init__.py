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
        assert self.n > max(itertools.chain(*inputs)), "an input is more than n"
        assert 0 <= min(itertools.chain(*inputs)), "an input is less than zero"
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

    def __eq__(self, other):
        if other is self:
            return True
        if not isinstance(other, type(self)):
            return False
        if self.states != other.states:
            return False
        if self.inputs != other.inputs:
            return False
        if self.funcs != other.funcs:
            return False
        return True

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

    def get_path_and_cycle(self, state=None):
        if state is None:
            state = self.states
        current_state = state
        next_state = self.next_state(current_state)
        seen = [current_state]
        while next_state not in seen:
            seen.append(next_state)
            current_state = next_state
            next_state = self.next_state(current_state)

        i = seen.index(next_state)
        return (seen[:i], seen[i:])

    def get_cycle(self, state=None):
        return self.get_path_and_cycle(state)[1]
