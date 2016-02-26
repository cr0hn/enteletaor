# -*- coding: utf-8 -*-

import six
import json
import redis
import base64
import logging
import binascii

from six.moves.cPickle import loads

log = logging.getLogger()


# ----------------------------------------------------------------------
def dump_keys(con):

	for key in con.keys('*'):
		key_type = con.type(key).lower()
		val = None
		if key_type in (b"kv", b"string"):
			val = con.get(key)
		if key_type in (b"hash", b"unacked", b"unacked_index"):
			val = con.hgetall(key)
		if key_type == b"zet":
			val = con.zrange(key, 0, -1)
		if key_type in (b"set", b"list"):
			val = con.mget(key)

		if val is not None:
			if isinstance(val, list):
				if val[0] is None:
					continue

			yield key, val


# --------------------------------------------------------------------------
# Human parsers
# --------------------------------------------------------------------------
def decode_object(key, val, ident=5):

	if isinstance(val, dict):

		log.error('    "%s":' % key)
		log.error("    {")
		_decode_object(val, ident)
		log.error("    }")
	else:
		log.error('    "%s": "%s"' % (key, val))


# ----------------------------------------------------------------------
def _decode_object(val, ident=5):
	"""
	Decode recursively string
	"""
	_new_ident = ident + 1

	for k, v in six.iteritems(val):
		# convert value to original type -> JSON
		try:
			_transformed_info = json.loads(v.decode("utf-8"))
		except (binascii.Error, AttributeError):
			_transformed_info = v

		# --------------------------------------------------------------------------
		# Try to display in "human" format
		# --------------------------------------------------------------------------
		if isinstance(_transformed_info, list):

			log.error('%s"%s":' % (" " * ident, k))

			for x in _transformed_info:
				if isinstance(x, dict):
					# Open data
					log.error("%s{" % (" " * _new_ident))

					_decode_object(x, _new_ident + 2)

					log.error("%s}" % (" " * _new_ident))

				else:
					log.error('%s"%s"' % ((" " * ident), x))

		# Dict handler
		elif isinstance(_transformed_info, dict):
			log.error('%s"%s":' % ((" " * ident), k))

			log.error("%s{" % (" " * _new_ident))

			_decode_object(v, _new_ident + 2)

			log.error("%s}" % (" " * _new_ident))

		# Basic type as value
		else:

			try:
				use_obj = _transformed_info.encode()
			except (TypeError, AttributeError, binascii.Error):
				use_obj = _transformed_info

			# Is Pickle encoded?
			try:
				_pickle_decoded = loads(use_obj)

				# Is pickled
				log.error('%s"%s":' % ((" " * ident), k))

				log.error("%s{" % (" " * _new_ident))

				_decode_object(_pickle_decoded, _new_ident + 2)

				log.error("%s}" % (" " * _new_ident))

			except Exception:

				# Try again decoding in base64
				try:
					_b64_decoded = base64.decodebytes(use_obj)

					# Is pickled
					log.error('%s"%s":' % ((" " * ident), k))

					log.error("%s{" % (" " * _new_ident))

					_decode_object(loads(_b64_decoded), _new_ident + 2)

					log.error("%s}" % (" " * _new_ident))

				except Exception:

					# Transform is not possible -> plain string
					log.error('%s"%s": "%s"' % ((" " * ident), k, use_obj))


# ----------------------------------------------------------------------
def action_redis_dump(config):
	"""
	Dump all redis information
	"""
	log.warning("  - Trying to connect with redis server...")

	# Connection with redis
	con = redis.StrictRedis(host=config.target, port=config.port, db=config.db)

	# Export results?
	export_file = None
	if config.export_results:
		export_file = open(config.export_results, "w")

	i = 0
	for i, t_val in enumerate(dump_keys(con)):
		key = t_val[0]
		val = t_val[1]

		# Display results?
		if config.no_screen is False:
			decode_object(key, val)

		# Dump to file?
		if export_file is not None:
			export_file.write(str(val))

	if i == 0:
		log.error("   - No information to dump in database")

	# Close file descriptor
	if export_file is not None:
		export_file.close()
