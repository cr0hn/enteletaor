# -*- coding: utf-8 -*-

import six
import redis
import logging

log = logging.getLogger()


# ----------------------------------------------------------------------
def action_redis_server_connected(config):
	"""
	Dump all redis information
	"""
	log.warning("  - Trying to connect with redis server...")

	# Connection with redis
	con = redis.StrictRedis(host=config.target, port=config.port, db=config.db)

	log.error("Connected users to '%s':" % config.target)

	for c in con.client_list():

		# Skip local host connections
		client = c['addr']
		db = c['db']

		log.error("  - %s (DB: %s)" % (client, db))

