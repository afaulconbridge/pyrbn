import json

# TODO also messagepack


class JSONDecodable:
    """
    This is a mixin class to enable decoding from JSON

    It builds an internal register of candidates, and checks each of them against the
    JSON provided. If exactly one is found, it is used to decode.

    Subclasses should implement _decode_test and _decode class methods to fit their
    own purposes
    """

    jsondecodable = []

    # see https://docs.python.org/3/reference/datamodel.html#customizing-class-creation
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.jsondecodable.append(cls)

    @classmethod
    def _decode_test(clzz, dct):
        return False

    @classmethod
    def _decode(clzz, dct):
        raise NotImplementedError

    @classmethod
    def object_hook(clzz, dct):
        # check each registered class to see if it is suitable
        cls_to_use = None
        for cls in clzz.jsondecodable:
            if cls._decode_test(dct):
                if cls_to_use:
                    # already found a suitable class, so error
                    raise JSONDecodableConflictException
                else:
                    cls_to_use = cls
        # if exactly one suitable class, use it
        if cls_to_use:
            return cls_to_use._decode(dct)
        else:
            raise ValueError


jsondecoder = json.JSONDecoder(object_hook=JSONDecodable.object_hook)


class JSONDecodableConflictException(Exception):
    pass
