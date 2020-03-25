from .basic import RBNBasic
from .cached import RBNCached

try:
    from .numpy import RBNNumpy
except ImportError:
    pass
    # unable to import numpy probably

# try to auto-detect the best implementation
RBN = RBNBasic


__all__ = ("RBN", "RBNBasic", "RBNCached", "RBNSorted")
