# -*- coding: utf-8 -*-

"""
This file contains command line actions for argparser
"""


# ----------------------------------------------------------------------
def parser_redis_dump(parser):
	"""
	Dump all redis database information
	"""
	gr = parser.add_argument_group("custom raw dump options")
	gr.add_argument("--no-raw", action="store_true", dest="no_raw", default=False,
	                help="do not show displays raw database info into screen")


# ----------------------------------------------------------------------
def parser_redis_server_disconnect(parser):
	gr = parser.add_argument_group("custom disconnect options")

	gr.add_argument("-c", action="store", dest="client", help="user to disconnect")
	gr.add_argument("--all", action="store_true", dest="disconnect_all", default=False,
	                help="disconnect all users")


# ----------------------------------------------------------------------
def parser_redis_server_cache_poison(parser):
	gr = parser.add_argument_group("custom poison options")

	gr.add_argument("--search", action="store_true", dest="search_cache", default=False,
	                help="try to find cache info stored in Redis")
	gr.add_argument("--cache-key", action="store", dest="cache_key",
	                help="try to poisoning using selected key")

	payload = parser.add_argument_group("payloads options")
	payload.add_argument("--payload", action="store", dest="poison_payload",
	                     help="try inject cmd inline payload")
	payload.add_argument("--file-payload", action="store", dest="poison_payload_file",
	                     help="try inject selected payload reading from a file")
	payload.add_argument("--replace-html", action="store", dest="new_html",
	                     help="replace cache content with selected file content")
