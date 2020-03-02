from .basic import RBNBasic
from .fast import RBNFast
from .numpy import RBNNumpy

# try to auto-detect the best implementation
RBN = RBNBasic
