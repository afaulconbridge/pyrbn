import json

from . import RBN

# TODO also messagepack


def rbn_to_json(rbn):
    """
    Use this like:
    json.dumps(rbn, default=rbn_to_json)
    """
    return json.dumps({"states": rbn.states, "inputs": rbn.inputs, "funcs": rbn.funcs})


def json_to_rbn(data, clzz=RBN):
    """
    Use like this:
    json.loads(data, object_hook=json_to_rbn)
    """
    return RBN(data["states"], data["inputs"], data["funcs"])
