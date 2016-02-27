# -*- coding: utf-8 -*-


import logging

from modules import IModule

from libs.core.structs import CommonData
from libs.core.models import StringField, SelectField

from .cmd_actions import parser_proc_raw_dump, parser_proc_list_process, parser_proc_inject_process
from .proc_remove import action_proc_remove
from .proc_raw_dump import action_proc_raw_dump
from .proc_list_process import action_proc_list_process
from .proc_inject_process import action_proc_inject_process

log = logging.getLogger()


# ----------------------------------------------------------------------
class ModuleModel(CommonData):
	target = StringField(required=True)
	db = StringField(default=None, label="only for Redis: database to use")
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
		'list-process': dict(
			help="list remote process and their params",
			cmd_args=parser_proc_list_process,
			action=action_proc_list_process
		),
		'inject': dict(
			help="list remote process and their params",
			cmd_args=parser_proc_inject_process,
			action=action_proc_inject_process
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
