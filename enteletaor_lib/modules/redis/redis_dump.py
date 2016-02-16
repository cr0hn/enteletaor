# -*- coding: utf-8 -*-

import redis
import logging
import pprint

log = logging.getLogger()


def dump_keys(con):

	for key in con.keys('*'):
		key_type = con.type(key).lower()
		val = None
		if key_type == b"kv":
			val = con.get(key)
		if key_type == b"hash":
			val = con.hgetall(key)
		if key_type == b"zet":
			val = con.zrange(key, 0, -1)
		if key_type == b"set":
			val = con.mget(key)

		if val is not None:
			if isinstance(val, list):
				if val[0] is None:
					continue

			yield val


# ----------------------------------------------------------------------
def action_redis_dump(config):
	"""
	Dump all redis information
	"""
	log.error("Trying to connect with redis server...")

	# Connection with redis
	con = redis.StrictRedis(host=config.target, port=config.port, db=config.db)

	# Export results?
	export_file = None
	if config.export_results:
		export_file = open(config.export_results, "w")

	for val in dump_keys(con):
		# Display results?
		if config.no_raw is False:
			log.warning(val)

		# Dump to file?
		if export_file is not None:
			export_file.write(str(val))

	# Close file descriptor
	if export_file is not None:
		export_file.close()
