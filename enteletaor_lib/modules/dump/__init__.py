# -*- coding: utf-8 -*-

import pickle
import logging

from time import sleep
from modules import IModule
from kombu import Connection
from kombu.simple import Empty
from kombu.exceptions import SerializationError

from ...libs.core.structs import CommonData, AppSettings
from ...libs.core.models import IntegerField, StringField, SelectField, validators

log = logging.getLogger()

REDIS = "10.211.55.69"


class ModuleModel(CommonData):
	interval = IntegerField(default=4)
	target = StringField([validators.required()])
	export_results = StringField(default="")
	import_results = StringField(default=None)
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

	name = "dump"
	description = "connect to remote server/s and dumps all available information"

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

		dump_from_celery(config)


# ----------------------------------------------------------------------
def dump_from_celery(config):
	"""
	Start dumping information
	"""
	URL = '%s://%s' % (config.broker_type, config.target)

	# with Connection('redis://%s' % REDIS) as conn:
	with Connection(URL) as conn:
		in_queue = conn.SimpleQueue('celery')

		while 1:
			try:
				while 1:
					message = in_queue.get(block=False, timeout=1)
					# message = in_queue.get(block=False, timeout=1)

					# --------------------------------------------------------------------------
					# Try to deserialize
					# --------------------------------------------------------------------------
					# Is Pickle info?
					try:
						deserialized = pickle.loads(message.body)
					except SerializationError:
						pass

					# Read info
					remote_process = deserialized['task'].split(".")[-1]
					remote_args = deserialized['args']

					# Show info
					_show_info(remote_process, remote_args)

			except Empty:
				# Queue is empty -> wait
				log.error("No more messages from server. Waiting for %s seconds and try again.." % config.interval)
				sleep(2)


# ----------------------------------------------------------------------
def _show_info(process, args):

		log.error("Found process information:")
		log.error("  -  Remote process name: '%s'" % process)
		log.error("  -  Input parameters:")
		for i, x in enumerate(args):
			log.error("      -> P%s: %s" % (i, x))
