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
import logging.handlers

from colorlog import ColoredFormatter


# ----------------------------------------------------------------------
def setup_logging():
    """
	Setup initial logging configuration
	"""
    from ...config import __tool_name__, DEBUG_LEVEL

    # Init logger
    logger = logging.getLogger()

    # Set log level
    logger.setLevel(abs(50 - (DEBUG_LEVEL if DEBUG_LEVEL < 5 else 5) * 10))

    # Set file log format
    file_format = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s', "%Y-%m-%d %H:%M:%S")
    log_file = logging.FileHandler(filename="%s.log" % __tool_name__)
    log_file.setFormatter(file_format)

    # Handler: console
    formatter = ColoredFormatter(
        "[ %(log_color)s*%(reset)s ] %(blue)s%(message)s",
        # "[ %(log_color)s%(levelname)-8s%(reset)s] %(blue)s%(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )
    log_console = logging.StreamHandler()
    log_console.setFormatter(formatter)

    # --------------------------------------------------------------------------
    # Add all of handlers to logger config
    # --------------------------------------------------------------------------
    logger.addHandler(log_console)
    logger.addHandler(log_file)
