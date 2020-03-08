import json

import pyrbn
import pyrbn.json


def test_to_json():

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
    rbn_json = '{"funcs": [[false, true, true, true], [true, true, false, false], [false, false, false, false], [false, false, false, true], [false, false, false, true]], "inputs": [[4, 0], [0, 4], [2, 3], [1, 2], [3, 1]], "states": [true, false, false, false, true]}'

    dumped = json.dumps(rbn, default=pyrbn.json.rbn_to_json)
    assert dumped == rbn_json, "JSON serialization mismatch"


def test_from_json():

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
    rbn_json = '{"funcs": [[false, true, true, true], [true, true, false, false], [false, false, false, false], [false, false, false, true], [false, false, false, true]], "inputs": [[4, 0], [0, 4], [2, 3], [1, 2], [3, 1]], "states": [true, false, false, false, true]}'

    loaded = json.loads(rbn_json, object_hook=pyrbn.json.json_to_rbn)
    print(loaded)
    assert loaded == rbn, "JSON deserialization mismatch"
