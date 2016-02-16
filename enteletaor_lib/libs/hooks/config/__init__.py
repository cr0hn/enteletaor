# -*- coding: utf-8 -*-

import logging

from .. import on_config_loaded

log = logging.getLogger()


# ----------------------------------------------------------------------
@on_config_loaded
def test_hook_config(parsed_args):
    """
    Hook for testing purposes
    """

    log.debug("[ HOOK ] Test_hook_config")


# ----------------------------------------------------------------------
@on_config_loaded
def set_log_level(parsed_args):
    """
    Setup log level from input user config from command line
    """

    if hasattr(parsed_args, "verbosity"):
        log.setLevel(abs(parsed_args.verbosity * 10) % 50)