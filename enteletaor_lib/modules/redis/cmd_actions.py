# -*- coding: utf-8 -*-

"""
This file contains command line actions for argparser
"""


# ----------------------------------------------------------------------
def parser_redis_dump(parser):
	"""
	Dump all redis database information
	"""
	parser.add_argument("--no-raw", action="store_true", dest="no_raw", default=False,
	                    help="do not show displays raw database info into screen")


# ----------------------------------------------------------------------
def parser_redis_server_disconnect(parser):
	parser.add_argument("-c", action="store", dest="client", help="user to disconnect")
	parser.add_argument("--all", action="store_true", dest="disconnect_all", default=False,
	                    help="disconnect all users")


# ----------------------------------------------------------------------
def parser_redis_server_cache_poison(parser):
	parser.add_argument("--search", action="store_true", dest="search_cache", default=False,
	                    help="try to find cache info stored in Redis")
	parser.add_argument("--cache-key", action="store", dest="cache_key",
	                    help="try to poisoning using selected key")

