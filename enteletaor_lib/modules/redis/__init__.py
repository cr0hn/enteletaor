# -*- coding: utf-8 -*-
#
# Enteletaor - https://github.com/cr0hn/enteletaor
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the
# following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import logging

from .. import IModule
from ...libs.core.structs import CommonData
from ...libs.core.models import StringField, IntegerField

from .redis_dump import action_redis_dump
from .redis_shell import action_redis_shell
from .redis_info import action_redis_server_info
from .redis_cache import action_redis_cache_poison
from .redis_discover_db import action_redis_discover_dbs
from .redis_clients import action_redis_server_connected
from .redis_disconnect import action_redis_server_disconnect
from .cmd_actions import parser_redis_dump, parser_redis_server_disconnect, parser_redis_server_cache_poison


log = logging.getLogger()


# ----------------------------------------------------------------------
class ModuleModel(CommonData):
	target = StringField(required=True)
	port = IntegerField(default=6379)
	db = IntegerField(default=0)


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
			help="discover all Redis DBs at server",
			action=action_redis_discover_dbs
		),
		'cache': dict(
			help="poison remotes cache using Redis server",
			action=action_redis_cache_poison,
			cmd_args=parser_redis_server_cache_poison
		),
	}

	name = "redis"
	description = "some attacks over Redis service"
