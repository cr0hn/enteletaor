# -*- coding: utf-8 -*-


"""
This file contains main data structures of project
"""

from .libs.core.structs import CommonInputExecutionData as _CED, CommonResultsExecutionData as _CERD


# --------------------------------------------------------------------------
class GlobalExecutionParameters(_CED):
    """Parameters while running"""


# --------------------------------------------------------------------------
class GlobalExecutionResults(_CERD):
    """Data structure for tools execution"""

