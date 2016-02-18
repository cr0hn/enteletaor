# -*- coding: utf-8 -*-

import os
import six
import json
import logging

from kombu import Connection

from .utils import list_remote_process

log = logging.getLogger()


# ----------------------------------------------------------------------
def get_param_type(value):
	"""
	Try to identify the parameter type by their value

	:return: string with type. Valid values: str, int, float, dict, list, bytes, object
	:rtype: str

	"""
	try:
		# Distinguish between int and float
		if int(value) == value:
			return "int"
		else:
			return "float"

	except ValueError:

		# If raises type must be string or complex data
		if type(value) == dict:
			return "dict"
		elif type(value) == list:
			return "list"
		elif type(value) == bytes:
			try:
				value.decode()

				return "bytes"
			except Exception:
				return "str"

		elif type(value) == str:
			return "str"
		else:
			return "object"


# ----------------------------------------------------------------------
def action_proc_list_process(config):

	log.warning("  - Trying to connect with server...")

	url = '%s://%s' % (config.broker_type, config.target)

	with Connection(url) as conn:
		in_queue = conn.SimpleQueue('celery')

		process_info = {}

		# Get remote process
		for remote_process, remote_args in list_remote_process(config, in_queue):

			if remote_process not in process_info:
				process_info[remote_process] = remote_args

		# Try to identify parameters types

		# Display info
		log.error("  - Remote process found:")
		for p, v in six.iteritems(process_info):
			log.error("     -> %s (%s)" % (
				p,
				", ".join("param_%s:%s" % (i, get_param_type(x)) for i, x in enumerate(v))
			))

		# Export to template enabled?
		if config.template is not None:
			log.warning("  - Building template...")

			export_data = []

			for p, v in six.iteritems(process_info):

				# Function name restriction?
				if config.function_name is not None and config.function_name != p:
					continue

				# Extract function params
				l_params = {}
				for i, l_p in enumerate(v):
					l_params = {
						'param_position': i,
						'param_type': get_param_type(l_p)
					}

				# Add to function information
				l_process = {
					'function': p,
					'parameters': l_params
				}

				# Add to all data

				export_data.append(l_process)

			# --------------------------------------------------------------------------
			# Save template
			# --------------------------------------------------------------------------
			# Build path in current dir
			export_path = "%s.json" % os.path.abspath(config.template)

			# dumps
			json.dump(export_data, open(export_path, "w"))

			log.error("  - Template saved at: '%s'" % export_path)
