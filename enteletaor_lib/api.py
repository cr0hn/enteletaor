# -*- coding: utf-8 -*-

"""
This file contains API calls and Data
"""

import six
import logging

from .data import *

__all__ = ["run_console", "run", "GlobalParameters"]

log = logging.getLogger()


# --------------------------------------------------------------------------
#
# Command line options
#
# --------------------------------------------------------------------------
def run_console(config):
    """
    :param config: GlobalParameters option instance
    :type config: `GlobalParameters`

    :raises: TypeError
    """
    if not isinstance(config, GlobalExecutionParameters):
        raise TypeError("Expected GlobalParameters, got '%s' instead" % type(config))

    logging.warning("[*] Starting Enteletaor execution")
    run(config)
    logging.warning("[*] Done!")


# ----------------------------------------------------------------------
#
# API call
#
# ----------------------------------------------------------------------
def run(config):
    """
    :param config: GlobalParameters option instance
    :type config: `GlobalParameters`

    :raises: TypeError
    """
    if not isinstance(config, GlobalExecutionParameters):
        raise TypeError("Expected GlobalParameters, got '%s' instead" % type(config))

    from .libs.core.structs import AppSettings

    # Run modules
    for mod_name, mod_obj in six.iteritems(AppSettings.modules):
        mod_obj().run(config)
