# -*- coding: utf-8 -*-

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
			con.client_kill(c)

			log.error("  - Disconnected client '%s'" % c)

	# Disconnect only one user
	else:
		# Check client format
		if config.client is None or ":" not in config.client:
			log.error("Invalid client format. Client must be format: IP:PORT, i.e: 10.211.55.2:61864")
			return

		try:
			_c = clients[config.client]

			con.client_kill(_c)

			log.error("  - Disconnected client '%s'" % _c)
		except KeyError:
			log.error("Client '%s' doesn't appear to be connected to server" % config.client)
