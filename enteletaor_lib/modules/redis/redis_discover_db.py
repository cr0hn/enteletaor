# -*- coding: utf-8 -*-

import six
import redis
import logging

log = logging.getLogger()


# ----------------------------------------------------------------------
def action_redis_discover_dbs(config):
	"""
	Dump all redis information
	"""
	log.warning("Trying to connect with redis server...")

	# Connection with redis
	con = redis.StrictRedis(host=config.target, port=config.port, db=config.db)

	log.error("Discovered '%s' DBs at '%s':" % (config.target, con.config_get("databases")['databases']))

	for db_name, db_content in six.iteritems(con.info("keyspace")):
		log.error("   - %s - %s keys" % (db_name.upper(), db_content['keys']))

	for i in six.moves.range((int(con.config_get("databases")['databases']) - len(con.info("keyspace")))):
		log.error("   - DB%s - Empty" % str(i))
