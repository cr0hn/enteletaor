# -*- coding: utf-8 -*-

import six

from kombu.simple import Empty
from six.moves.cPickle import loads
from kombu.exceptions import SerializationError


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
# Import/export process information
# ----------------------------------------------------------------------
def export_process(process_info, config):
	"""
	Export process info to json file

	:return: return a dict JSON compatible
	:rtype: dict
	"""

	export_data = []

	for p, v in six.iteritems(process_info):

		# Function name restriction?
		if config.function_name is not None and config.function_name != p:
			continue

		# Extract function params
		params = []
		for i, l_p in enumerate(v):
			l_params = {
				'param_position': i,
				'param_type': get_param_type(l_p),
				'param_value': None
			}
			params.append(l_params)

		# Add to function information
		l_process = {
			'function': p,
			'parameters': params
		}

		# Add to all data
		export_data.append(l_process)

	return export_data


# ----------------------------------------------------------------------
def get_remote_messages(config, queue, fill=True, block=False):
	"""
	Get all messages from queue without removing from it

	:return: yield raw deserialized messages
	:rtype: json
	"""

	to_inject = []

	try:
		while 1:
			message = queue.get(block=False, timeout=1)

			# --------------------------------------------------------------------------
			# Try to deserialize
			# --------------------------------------------------------------------------
			# Is Pickle info?
			try:
				deserialized = loads(message.body)
			except SerializationError:
				pass

			yield deserialized

			to_inject.append(deserialized)

	except Empty:
		# When Queue is Empty -> reinject all removed messages
		if fill is True:
			for x in to_inject:
				queue.put(x, serializer="pickle")


# ----------------------------------------------------------------------
def list_remote_process(config, queue):
	"""
	Get all messages from queue without removing from it

	:return: yield two values: remote_process name, remote args
	:rtype: str, set
	"""

	already_processed = set()

	for deserialized in get_remote_messages(config, queue):

		msg_id = deserialized['id']

		# Read info
		if msg_id not in already_processed:

			remote_process = deserialized['task'].split(".")[-1]
			remote_args = deserialized['args']

			# Store as processed
			already_processed.add(msg_id)

			yield remote_process, remote_args
