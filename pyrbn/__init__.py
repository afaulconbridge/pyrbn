from .basic import RBNBasic
from .fast import RBNFast

try:
    from .numpy import RBNNumpy
except ImportError:
    pass
    # unable to import numpy probably

# try to auto-detect the best implementation
RBN = RBNBasic
