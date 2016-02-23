# -*- coding: utf-8 -*-

import logging

__tool__ = "enteletaor"

log = logging.getLogger()


# ----------------------------------------------------------------------
def main():

    from .libs.core.cmd import build_arg_parser
    from .api import GlobalExecutionParameters, run_console

    # Build command line parser
    parser = build_arg_parser()
    parsed_args = parser.parse_args_and_run_hooks()

    # Build config
    config = GlobalExecutionParameters.from_argparser(parsed_args)

    try:
        # Start!
        run_console(config)
    except KeyboardInterrupt:
        log.warning("CTRL+C caught. Exiting...")
    except Exception as e:
        log.critical("Unhandled exception: %s" % str(e))
        log.debug("", exc_info=True)

if __name__ == "__main__" and __package__ is None:
    #region main

    # --------------------------------------------------------------------------
    # INTERNAL USE: DO NOT MODIFY THIS SECTION!!!!!
    # --------------------------------------------------------------------------
    import sys, os
    sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    __import__("enteletaor_lib")
    __package__ = str("enteletaor_lib")
    # --------------------------------------------------------------------------
    # END INTERNAL USE
    # --------------------------------------------------------------------------

    #endregion

    main()
