from typing import Tuple

import cachetools  # type: ignore

from .basic import RBNBasic


class RBNCached(RBNBasic):
    def __init__(self, states: Tuple[bool], inputs: Tuple[int], funcs: Tuple[Tuple[bool]]):
        super(RBNCached, self).__init__(states, inputs, funcs)
        self.cache_state = cachetools.LRUCache(32768)

    @cachetools.cachedmethod(lambda self: self.cache_state)
    def next_state(self, state=None):
        return super(RBNCached, self).next_state(state)
