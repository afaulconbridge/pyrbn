import random

import pyrbn


def test_from_random():
    rng = random.Random(42)
    rbn = pyrbn.RBN.from_random(rng, 5)
    assert rbn is not None
    assert rbn.n == 5
    print(rbn)
    print(rbn.next_state())
    print(rbn.find_cycle())
    1 / 0
