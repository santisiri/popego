"""\
This module is deprecated. Please update your code to use 
``authkit.authorize.pylons_adaptors`` instead of this module.
"""
import warnings
warnings.warn(
    """This module is deprecated. Please update your code to use ``authkit.authorize.pylons_adaptors`` instead of this module.""", 
    DeprecationWarning, 
    2
)
from authkit.authorize.pylons_adaptors import *
