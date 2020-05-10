import functools
import itertools
import json
from typing import List, Sequence, Tuple

from .json import JSONDecodable


class BooleanNetworkStructure(JSONDecodable):
    # TODO use __new__ and weakref to prevent duplicates
    # see https://docs.python.org/3/reference/datamodel.html#object.__new__
    # see https://docs.python.org/3/library/weakref.html#weakref.WeakValueDictionary
    inputs: Tuple[Tuple[int]]
    funcs: Tuple[Tuple[bool]]
    n: int
    k: int
    pows: List[int] = []

    __hash = None  # store hash once calculated
    __key = ()  # store common key used for equality, ordering, hashing

    def __init__(self, inputs: Sequence[Sequence[int]], funcs: Sequence[Sequence[bool]]):
        self.n = len(inputs)
        assert self.n == len(inputs)
        assert self.n > 0
        self.k = len(inputs[0])
        assert self.k == max((len(i) for i in inputs))
        assert self.k == min((len(i) for i in inputs))
        assert self.n > max(itertools.chain(*inputs)), "an input is more than n"
        assert 0 <= min(itertools.chain(*inputs)), "an input is less than zero"
        assert 2 ** self.k == max((len(x) for x in funcs)), "funcs must be 2**k long"
        assert 2 ** self.k == min((len(x) for x in funcs)), "funcs must be 2**k long"

        self.inputs = tuple(map(tuple, inputs))
        self.funcs = tuple(map(tuple, funcs))

        # pre compute powers of two on the class
        while self.k >= len(self.pows):
            self.pows.append(2 ** (len(self.pows)))

        self.__key = (self.inputs, self.funcs)

    @classmethod
    def from_random(clzz, rng, n=5, k=2):
        inputs = tuple(zip(*(list(rng.sample(range(n), n)) for i in range(k))))
        funcs = tuple((tuple((rng.random() >= 0.5 for j in range(2 ** k))) for i in range(n)))
        return clzz(inputs, funcs)

    def next_state(self, state):
        return tuple(
            (self.funcs[i][sum((self.pows[j] for j in range(self.k) if state[self.inputs[i][j]]))] for i in range(self.n))
        )

    def __eq__(self, other):
        """
        Will only return true if nodes have the same order
        i.e. does *NOT* respect isomorphism
        """
        if self is other:
            return True

        return self.__key == other.__key

    def __lt__(self, other):
        """
        Will only work as intended if nodes have the same order
        i.e. does *NOT* respect isomorphism
        """
        if self is other:
            return False

        return self.__key < other.__key

    def __hash__(self):
        """
        Will only work as intended if nodes have the same order
        i.e. does *NOT* respect isomorphism
        """
        if not self.__hash:
            self.__hash = hash(self.__key)

        return self.__hash

    def __repr__(self):
        return "{}({}, {})".format(type(self).__name__, self.inputs, self.funcs)

    class JSONEncoder(json.JSONEncoder):
        def default(self, obj):
            return {"inputs": obj.inputs, "funcs": obj.funcs}

    jsonencoder = JSONEncoder()

    @classmethod
    def _decode_test(clzz, dct):
        return "inputs" in dct and "funcs" in dct

    @classmethod
    def _decode(clzz, dct):
        return clzz(dct["inputs"], dct["funcs"])


@functools.total_ordering
class BooleanNetwork(JSONDecodable):
    # TODO use __new__ and weakref to prevent duplicates
    # see https://docs.python.org/3/reference/datamodel.html#object.__new__
    # see https://docs.python.org/3/library/weakref.html#weakref.WeakValueDictionary
    states: Tuple[bool]
    struct: BooleanNetworkStructure

    __hash = None  # store hash once calculated
    __key = ()  # store common key used for equality, ordering, hashing

    def __init__(self, states: Sequence[bool], struct: BooleanNetworkStructure):
        self.states = tuple(states)
        self.struct = struct

        self.__key = (self.states, self.struct)

    @classmethod
    def from_random(clzz, rng, n=5, k=2):
        states = [rng.random() >= 0.5 for i in range(n)]
        struct = BooleanNetworkStructure.from_random(rng)
        return clzz(states, struct)

    @property
    def n(self):
        return self.struct.n

    @property
    def k(self):
        return self.struct.k

    @property
    def inputs(self):
        return self.struct.inputs

    @property
    def funcs(self):
        return self.struct.funcs

    def __eq__(self, other):
        """
        Will only return true if nodes have the same order
        i.e. does *NOT* respect isomorphism
        """
        if self is other:
            return True

        return self.__key == other.__key

    def __lt__(self, other):
        """
        Will only work as intended if nodes have the same order
        i.e. does *NOT* respect isomorphism
        """
        if self is other:
            return False

        return self.__key < other.__key

    def __hash__(self):
        """
        Will only work as intended if nodes have the same order
        i.e. does *NOT* respect isomorphism
        """
        if not self.__hash:
            self.__hash = hash(self.__key)

        return self.__hash

    def __repr__(self):
        return "{}({}, {})".format(type(self).__name__, self.states, self.struct)

    def next_state(self, state=None):
        if state is None:
            state = self.states
        return self.struct.next_state(state)

    def get_path_and_cycle(self, state=None):
        if state is None:
            state = self.states

        seen = [state]
        seen_set = set(seen)

        current_state = state
        next_state = self.next_state(current_state)

        while next_state not in seen_set:
            seen.append(next_state)
            seen_set.add(next_state)

            current_state = next_state
            next_state = self.next_state(current_state)

        i = seen.index(next_state)
        return (tuple(seen[:i]), tuple(seen[i:]))

    def get_cycle(self, state=None):
        return self.get_path_and_cycle(state)[1]

    jsonencoder = json.JSONEncoder(
        default=lambda obj: {"states": obj.states, "struct": obj.struct.jsonencoder.default(obj.struct)}
    )

    @classmethod
    def _decode_test(clzz, dct):
        return "states" in dct and "struct" in dct

    @classmethod
    def _decode(clzz, dct):
        return clzz(dct["states"], dct["struct"])
