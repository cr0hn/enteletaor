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
	log.warning("  - Trying to connect with redis server...")

	# Connection with redis
	con = redis.StrictRedis(host=config.target, port=config.port, db=config.db)

	log.error("Discovered '%s' DBs at '%s':" % (config.target, con.config_get("databases")['databases']))

	discovered_dbs = set()

	for db_name, db_content in six.iteritems(con.info("keyspace")):
		log.error("   - %s - %s keys" % (db_name.upper(), db_content['keys']))

		discovered_dbs.add(db_name.upper())

	for i in six.moves.range((int(con.config_get("databases")['databases']) - len(con.info("keyspace")))):

		_db_name = "DB%s" % i

		if _db_name in discovered_dbs:
			continue

		log.error("   - %s - Empty" % _db_name)
