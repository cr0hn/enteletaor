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

"""
This file contains command line actions for argparser
"""


# ----------------------------------------------------------------------
def parser_proc_raw_dump(parser):
	gr = parser.add_argument_group("custom raw dump options")

	gr.add_argument("--streaming", action="store_true", dest="streaming_mode", default=False,
	                help="although all information be dumped do not stop")
	gr.add_argument("-I", dest="interval", type=float, default=4,
	                help="timeout interval between tow connections")
	gr.add_argument("--output", dest="output", help="store dumped information into file")


# ----------------------------------------------------------------------
def parser_proc_list_tasks(parser):
	parser.add_argument("-N", "--no-stream", dest="no_stream", action="store_true", default=False,
	                    help="force to not listen until message is received")

	gr = parser.add_argument_group("process exporting options")

	gr.add_argument("-T", "--make-template", dest="template", type=str,
	                help="export process as a JSON template format, ready to make injections")
	gr.add_argument("-F", "--function-name", dest="function_name", type=str,
	                help="only export this function name")


# ----------------------------------------------------------------------
def parser_taks_inject_process(parser):
	gr = parser.add_argument_group("process importing options")

	gr.add_argument("-f", "--function-file", dest="function_files", type=str, required=True,
	                help="import process info from JSON file")
