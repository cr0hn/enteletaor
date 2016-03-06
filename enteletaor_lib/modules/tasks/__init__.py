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
from ...libs.core.models import StringField, SelectField

from .cmd_actions import parser_proc_raw_dump, parser_proc_list_tasks, parser_taks_inject_process
from .tasks_remove import action_proc_remove
from .tasks_raw_dump import action_proc_raw_dump
from .tasks_list_process import action_proc_list_tasks
from .tasks_inject_process import action_task_inject_process

log = logging.getLogger()


# ----------------------------------------------------------------------
class ModuleModel(CommonData):
	target = StringField(required=True)
	db = StringField(default=None, label="only for Redis: database to use")
	process_manager = SelectField(default="celery", choices=[("celery", "Celery")],
	                              label="process manager running in backend")
	broker_type = SelectField(default="redis", choices=[
		("redis", "Redis server"),
		("zmq", "ZeroMQ"),
		("amqp", "RabbitMQ broker")
	])


# ----------------------------------------------------------------------
class RemoteProcessModule(IModule):
	"""
	Try to extract information from remote processes
	"""
	__model__ = ModuleModel
	__submodules__ = {
		'raw-dump': dict(
			help="dump raw remote information process",
			cmd_args=parser_proc_raw_dump,
			action=action_proc_raw_dump
		),
		'list-tasks': dict(
			help="list remote tasks and their params",
			cmd_args=parser_proc_list_tasks,
			action=action_proc_list_tasks
		),
		'inject': dict(
			help="inject a new task into broker",
			cmd_args=parser_taks_inject_process,
			action=action_task_inject_process
		),
		'remove': dict(
			help="remove remote processes in server",
			cmd_args=None,
			action=action_proc_remove
		),
	}

	name = "tasks"
	description = "try to discover and handle processes in remote MQ/Brokers"

	# ----------------------------------------------------------------------
	def run(self, config):
		# --------------------------------------------------------------------------
		# Ver dirty monkey patch to avoid kombu write into screen
		# --------------------------------------------------------------------------
		try:
			import sys
			sys.stderr = open("/dev/null")
		except IOError:
			pass

		super(RemoteProcessModule, self).run(config)
