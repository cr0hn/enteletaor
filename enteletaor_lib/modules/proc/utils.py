# -*- coding: utf-8 -*-

from kombu.simple import Empty
from six.moves.cPickle import loads
from kombu.exceptions import SerializationError


# ----------------------------------------------------------------------
def get_remote_messages(config, queue):
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
