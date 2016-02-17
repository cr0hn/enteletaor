# -*- coding: utf-8 -*-

import logging

from modules import IModule
from libs.core.models import StringField, IntegerField
from libs.core.structs import CommonData

from .cmd_actions import parser_redis_dump, parser_redis_server_disconnect
from .redis_dump import action_redis_dump
from .redis_info import action_redis_server_info
from .redis_clients import action_redis_server_connected
from .redis_disconnect import action_redis_server_disconnect
from .redis_shell import action_redis_shell
from .redis_discover_db import action_redis_discover_dbs


log = logging.getLogger()


# ----------------------------------------------------------------------
class ModuleModel(CommonData):
	target = StringField(required=True)
	port = IntegerField(default=6379)
	db = IntegerField(default=0)
	export_results = StringField()


# ----------------------------------------------------------------------
class RedisModule(IModule):
	"""
	Try to extract information from remote processes
	"""
	__model__ = ModuleModel
	__submodules__ = {
		'dump': dict(
			help="dumps all keys in Redis database",
			cmd_args=parser_redis_dump,
			action=action_redis_dump
		),
		'info': dict(
			help="open a remote shell through the Redis server",
			action=action_redis_server_info
		),
		'connected': dict(
			help="get connected users to Redis server",
			action=action_redis_server_connected
		),
		'disconnect': dict(
			help="disconnect one or all users from Redis server",
			cmd_args=parser_redis_server_disconnect,
			action=action_redis_server_disconnect
		),
		'discover-dbs': dict(
			help="discover all redis DBs at server",
			action=action_redis_discover_dbs
		),
		# 'shell': dict(
		# 	help="open a remote os shell through the Redis server",
		# 	action=action_redis_shell
		# ),
	}

	name = "redis"
	description = "some attacks over Redis service"