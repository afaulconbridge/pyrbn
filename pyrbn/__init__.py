from .basic import RBNBasic

try:
    from .numpy import RBNNumpy
except ImportError:
    pass
    # unable to import numpy probably

# try to auto-detect the best implementation
RBN = RBNBasic
