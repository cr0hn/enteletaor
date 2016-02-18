# -*- coding: utf-8 -*-

import six
import redis
import logging

log = logging.getLogger()


# ----------------------------------------------------------------------
def action_redis_server_info(config):
	"""
	Dump all redis information
	"""
	log.warning("  - Trying to connect with redis server...")

	# Connection with redis
	con = redis.StrictRedis(host=config.target, port=config.port, db=config.db)

	log.error("Config for server '%s':" % config.target)

	for x, y in six.iteritems(con.config_get()):
		log.error("  - %s: %s" % (x, y))

