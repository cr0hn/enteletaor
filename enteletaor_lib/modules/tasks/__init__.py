# -*- coding: utf-8 -*-


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
