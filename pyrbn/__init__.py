from .basic import BooleanNetwork, BooleanNetworkStructure

try:
    from .numpy import RBNNumpy
except ImportError:
    pass
    # probably unable to import numpy

__all__ = ("BooleanNetwork", "BooleanNetworkStructure")
