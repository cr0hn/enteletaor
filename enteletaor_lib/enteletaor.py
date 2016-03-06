# -*- coding: utf-8 -*-
#
# Enteletaor - https://github.com/cr0hn/enteletaor
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the
# following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

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
