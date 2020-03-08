from . import RBN

# TODO also messagepack


def rbn_to_json(rbn):
    """
    Use this like:
    json.dumps(rbn, default=rbn_to_json)
    """
    if isinstance(rbn, RBN):
        return {"funcs": rbn.funcs, "inputs": rbn.inputs, "states": rbn.states}
    else:
        raise TypeError("Non RBN object")


def json_to_rbn(data, clazz=RBN):
    """
    Use like this:
    json.loads(data, object_hook=json_to_rbn)
    """
    return clazz(data["states"], data["inputs"], data["funcs"])
