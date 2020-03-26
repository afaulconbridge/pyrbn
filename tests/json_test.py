import json

import pyrbn
import pyrbn.json


def test_to_json():

    rbn = pyrbn.BooleanNetwork(
        (True, False, False, False, True),
        pyrbn.BooleanNetworkStructure(
            ((4, 0), (0, 4), (2, 3), (1, 2), (3, 1)),
            (
                (False, True, True, True),
                (True, True, False, False),
                (False, False, False, False),
                (False, False, False, True),
                (False, False, False, True),
            ),
        ),
    )
    rbn_json = """{
    "states": [true, false, false, false, true],
    "struct": {
        "inputs": [[4, 0], [0, 4], [2, 3], [1, 2], [3, 1]],
        "funcs": [
            [false, true, true, true],
            [true, true, false, false],
            [false, false, false, false],
            [false, false, false, true],
            [false, false, false, true]]
    }
}"""

    dumped = rbn.jsonencoder.encode(rbn)
    rbn_dict = json.loads(rbn_json)
    dumped_dict = json.loads(dumped)

    assert rbn_dict == dumped_dict, "JSON serialization mismatch"


def test_from_json():

    rbn = pyrbn.BooleanNetwork(
        (True, False, False, False, True),
        pyrbn.BooleanNetworkStructure(
            ((4, 0), (0, 4), (2, 3), (1, 2), (3, 1)),
            (
                (False, True, True, True),
                (True, True, False, False),
                (False, False, False, False),
                (False, False, False, True),
                (False, False, False, True),
            ),
        ),
    )
    rbn_json = """{
    "states": [true, false, false, false, true],
    "struct": {
        "inputs": [[4, 0], [0, 4], [2, 3], [1, 2], [3, 1]],
        "funcs": [
            [false, true, true, true],
            [true, true, false, false],
            [false, false, false, false],
            [false, false, false, true],
            [false, false, false, true]]
    }
}"""

    loaded = pyrbn.json.jsondecoder.decode(rbn_json)
    assert rbn == loaded, "JSON deserialization mismatch"
