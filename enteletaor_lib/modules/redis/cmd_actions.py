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
def parser_redis_dump(parser):
	"""
	Dump all redis database information
	"""
	gr = parser.add_argument_group("custom raw dump options")
	gr.add_argument("--no-screen", action="store_true", dest="no_screen", default=False,
	                help="do not show displays raw database info into screen")
	gr.add_argument("-e", "--export-results", dest="export_results",
	                help="export dumped information results")


# ----------------------------------------------------------------------
def parser_redis_server_disconnect(parser):
	gr = parser.add_argument_group("custom disconnect options")

	gr.add_argument("-c", action="store", dest="client", help="user to disconnect")
	gr.add_argument("--all", action="store_true", dest="disconnect_all", default=False,
	                help="disconnect all users")


# ----------------------------------------------------------------------
def parser_redis_server_cache_poison(parser):
	gr = parser.add_argument_group("custom poison options")

	gr.add_argument("--search", action="store_true", dest="search_cache", default=False,
	                help="try to find cache info stored in Redis")
	gr.add_argument("--cache-key", action="store", dest="cache_key",
	                help="try to poisoning using selected key")

	payload = parser.add_argument_group("payloads options")
	payload.add_argument("-P", "--poison", action="store_true", dest="poison", default=False,
	                     help="enables cache poisoning")
	payload.add_argument("--payload", action="store", dest="poison_payload",
	                     help="try inject cmd inline payload")
	payload.add_argument("--file-payload", action="store", dest="poison_payload_file",
	                     help="try inject selected payload reading from a file")
	payload.add_argument("--replace-html", action="store", dest="new_html",
	                     help="replace cache content with selected file content")
