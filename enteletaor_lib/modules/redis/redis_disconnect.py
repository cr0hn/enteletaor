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

import six
import redis
import logging

log = logging.getLogger()


# ----------------------------------------------------------------------
def action_redis_server_disconnect(config):
	"""
	Disconnect one or more users from server
	"""
	log.warning("  - Trying to connect with redis server...")

	# Connection with redis
	con = redis.StrictRedis(host=config.target, port=config.port, db=config.db)

	clients = {x['addr']: x['addr'] for x in con.client_list()}

	# Disconnect all clients?
	if config.disconnect_all:
		for c in clients:
			try:
				con.client_kill(c)

				log.error("  - Client '%s' was disconnected" % c)
			except redis.exceptions.ResponseError:
				log.error("  - Client '%s' is not connected" % c)


	# Disconnect only one user
	else:
		# Check client format
		if config.client is None or ":" not in config.client:
			log.error("  <!> Invalid client format. Client must be format: IP:PORT, i.e: 10.211.55.2:61864")
			return

		try:
			_c = clients[config.client]
			try:
				con.client_kill(_c)

				log.error("  - Client '%s' was disconnected" % _c)
			except redis.exceptions.ResponseError:
				log.error("  - Client '%s' is not connected" % _c)

		except KeyError:
			log.error("  <!> Client '%s' doesn't appear to be connected to server" % config.client)
