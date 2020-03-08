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
        (
            (False, True, True, True),
            (True, True, False, False),
            (False, False, False, False),
            (False, False, False, True),
            (False, False, False, True),
        ),
    )
    next_state = rbn.next_state()
    assert len(next_state) == 5
    assert next_state == (True, False, False, False, False)


def test_path_and_cycle():
    rbn = pyrbn.RBN(
        (True, False, False, False, True),
        ((4, 0), (0, 4), (2, 3), (1, 2), (3, 1)),
        (
            (False, True, True, True),
            (True, True, False, False),
            (False, False, False, False),
            (False, False, False, True),
            (False, False, False, True),
        ),
    )
    path, cycle = rbn.get_path_and_cycle()
    assert len(path) == 2
    assert len(cycle) == 1


def test_eq():
    rbna = pyrbn.RBN(
        (True, False, False, False, True),
        ((4, 0), (0, 4), (2, 3), (1, 2), (3, 1)),
        (
            (False, True, True, True),
            (True, True, False, False),
            (False, False, False, False),
            (False, False, False, True),
            (False, False, False, True),
        ),
    )
    rbnb = pyrbn.RBN(
        (True, False, False, False, True),
        ((4, 0), (0, 4), (2, 3), (1, 2), (3, 1)),
        (
            (False, True, True, True),
            (True, True, False, False),
            (False, False, False, False),
            (False, False, False, True),
            (False, False, False, True),
        ),
    )
    assert rbna is rbna
    assert rbna == rbna
    assert hash(rbna) == hash(rbna)
    assert rbna == rbnb
    assert hash(rbna) == hash(rbnb)
    assert not rbna != rbnb


def test_lt():
    rbna = pyrbn.RBN(
        (True, False, False, False, True),
        ((4, 0), (0, 4), (2, 3), (1, 2), (3, 1)),
        (
            (False, True, True, True),
            (True, True, False, False),
            (False, False, False, False),
            (False, False, False, True),
            (False, False, False, True),
        ),
    )
    rbnb = pyrbn.RBN(
        (False, False, False, False, True),
        ((4, 0), (0, 4), (2, 3), (1, 2), (3, 1)),
        (
            (False, True, True, True),
            (True, True, False, False),
            (False, False, False, False),
            (False, False, False, True),
            (False, False, False, True),
        ),
    )
    assert rbna != rbnb
    assert rbna > rbnb
    assert rbnb < rbna
    rbnc = pyrbn.RBN(
        (True, False, False, False, True),
        ((4, 0), (0, 4), (2, 3), (1, 1), (3, 1)),
        (
            (False, True, True, True),
            (True, True, False, False),
            (False, False, False, False),
            (False, False, False, True),
            (False, False, False, True),
        ),
    )
    assert rbna != rbnc
    assert rbna > rbnc
    assert rbnc < rbna
