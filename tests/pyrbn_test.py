import random

import pyrbn


def test_from_random():
    rng = random.Random(42)
    rbn = pyrbn.RBN.from_random(rng, 5)
    assert rbn is not None
    assert rbn.n == 5


def test_next_state():
    rbn = pyrbn.RBN(
        (True, False, False, False, True),
        ((4, 0), (0, 4), (2, 3), (1, 2), (3, 1)),
        [
            {
                (True, True): True,
                (True, False): True,
                (False, True): True,
                (False, False): False,
            },
            {
                (True, True): False,
                (True, False): False,
                (False, True): True,
                (False, False): True,
            },
            {
                (True, True): False,
                (True, False): False,
                (False, True): False,
                (False, False): False,
            },
            {
                (True, True): True,
                (True, False): False,
                (False, True): False,
                (False, False): False,
            },
            {
                (True, True): False,
                (True, False): False,
                (False, True): False,
                (False, False): False,
            },
        ],
    )
    next_state = rbn.next_state()
    assert len(next_state) == 5
    assert next_state == (True, False, False, False, False)
