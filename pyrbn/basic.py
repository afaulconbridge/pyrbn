import itertools
from typing import List, Tuple


class RBNBasic:
    states: Tuple[bool] = ()
    inputs: Tuple[Tuple[int]] = ()
    funcs: Tuple[Tuple[bool]] = ()
    pows: List[int] = []

    def __init__(
        self, states: Tuple[bool], inputs: Tuple[int], funcs: Tuple[Tuple[bool]]
    ):
        self.n = len(states)
        assert self.n == len(inputs)
        assert self.n > 0
        self.k = len(inputs[0])
        assert self.k == max((len(i) for i in inputs))
        assert self.k == min((len(i) for i in inputs))
        assert self.n > max(itertools.chain(*inputs)), "an input is more than n"
        assert 0 <= min(itertools.chain(*inputs)), "an input is less than zero"
        assert 2 ** self.k == max((len(x) for x in funcs)), "funcs must be 2**k long"
        assert 2 ** self.k == min((len(x) for x in funcs)), "funcs must be 2**k long"

        # TODO sort nodes on creation
        self.states = tuple(states)
        self.inputs = tuple(inputs)
        self.funcs = tuple(map(tuple, funcs))

        # pre compute powers of two
        while self.k >= len(self.pows):
            self.pows.append(2 ** (len(self.pows)))

    @classmethod
    def from_random(clzz, rng, n=5, k=2):
        states = [rng.random() >= 0.5 for i in range(n)]
        inputs = tuple(zip(*(list(rng.sample(range(n), n)) for i in range(k))))
        funcs = tuple(
            (tuple((rng.random() >= 0.5 for j in range(2 ** k))) for i in range(n))
        )
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
            (
                self.funcs[i][
                    sum(
                        (
                            self.pows[j]
                            for j in range(self.k)
                            if state[self.inputs[i][j]]
                        )
                    )
                ]
                for i in range(self.n)
            )
        )

    def get_path_and_cycle(self, state=None):
        if state is None:
            state = self.states
        current_state = state
        next_state = self.next_state(current_state)
        seen = [current_state]
        seen_set = set(seen)
        while next_state not in seen_set:
            seen.append(next_state)
            seen_set.add(tuple(next_state))
            current_state = next_state
            next_state = self.next_state(current_state)

        i = seen.index(next_state)
        return (seen[:i], seen[i:])

    def get_cycle(self, state=None):
        return self.get_path_and_cycle(state)[1]
