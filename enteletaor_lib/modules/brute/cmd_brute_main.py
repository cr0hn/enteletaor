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

import os
import six
import logging

from .utils import get_server_type

if six.PY2:
	from .cracker import cracking
else:
	# from .cracker3 import cracking
	from .cracker import cracking

# Reconfigure AMQP LOGGER
logging.getLogger('amqp').setLevel(100)

log = logging.getLogger()


# ----------------------------------------------------------------------
def cmd_brute_main(config):

	# --------------------------------------------------------------------------
	# Check requisites
	# --------------------------------------------------------------------------
	if not config.target:
		logging.error("  <!> target option, '-t', is required")
		return
	if not config.wordlist:
		logging.error("  <!> wordlist option, '-w', is required")
		return

	# Fix wordlist path
	if not os.path.exists(config.wordlist):
		wordlist_base = os.path.join(os.path.dirname(__file__),
		                             "..",
		                             "..",
		                             "resources",
		                             "wordlist")

		# Try to find into internal wordlists
		internal_wordlists = [x for x in os.listdir(os.path.abspath(wordlist_base)) if "readme" not in x.lower()]

		wordlist_choice = "%s.txt" % config.wordlist if ".txt" not in config.wordlist else config.wordlist

		# Is wordlist available?
		if wordlist_choice not in internal_wordlists:
			log.error("  <!> Wordlist '%s' not found." % wordlist_choice)
			return

		# Fix wordlist path
		config.wordlist = os.path.abspath(os.path.join(wordlist_base, wordlist_choice))

	# --------------------------------------------------------------------------
	# Preparing scan
	# --------------------------------------------------------------------------
	server_type, status, port = get_server_type(config)

	if status != "closed":
		log.error("  - Detected '%s' server with '%s'." % ('unknown' if server_type is None else server_type, status))

	if server_type.lower() == "rabbitmq":
		log.error("  - Set user to '%s'" % config.user)

	# --------------------------------------------------------------------------
	# Do brute
	# --------------------------------------------------------------------------
	if status == "auth":
		log.error("  - Starting bruteforcer using wordlist: '%s'" % config.wordlist)
		cracking(server_type, port, config)
	elif status == "open":
		log.error("  - '%s' '%s' server is open. No password cracking need" % (server_type, config.target))
	else:
		log.error("  - Not detected brokers in '%s'." % config.target)
