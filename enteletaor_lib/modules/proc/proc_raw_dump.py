# -*- coding: utf-8 -*-

import six
import logging

from time import sleep
from kombu import Connection
from kombu.simple import Empty
from six.moves.cPickle import loads
from kombu.exceptions import SerializationError

log = logging.getLogger()


# ----------------------------------------------------------------------
def action_proc_raw_dump(config):

	url = '%s://%s' % (config.broker_type, config.target)

	# with Connection('redis://%s' % REDIS) as conn:
	with Connection(url) as conn:
		in_queue = conn.SimpleQueue('celery')

		to_inject = []
		already_processed = set()

		while 1:
			try:
				while 1:
					message = in_queue.get(block=False, timeout=1)

					# --------------------------------------------------------------------------
					# Try to deserialize
					# --------------------------------------------------------------------------
					# Is Pickle info?
					try:
						deserialized = loads(message.body)
					except SerializationError:
						pass

					msg_id = deserialized['id']

					# Read info
					if msg_id not in already_processed:

						remote_process = deserialized['task'].split(".")[-1]
						remote_args = deserialized['args']

						# Show info
						log.error("Found process information:")
						log.error("  -  Remote process name: '%s'" % remote_process)
						log.error("  -  Input parameters:")
						for i, x in enumerate(remote_args):
							log.error("      -> P%s: %s" % (i, x))

						# Store as processed
						already_processed.add(msg_id)

					# --------------------------------------------------------------------------
					# Store message to re-send
					# --------------------------------------------------------------------------
					to_inject.append(deserialized)

			except Empty:
				# When Queue is Empty -> reinject all removed messages
				for x in to_inject:
					in_queue.put(x, serializer="pickle")

				# Queue is empty -> wait
				if config.tail_mode:
					log.error("No more messages from server. Waiting for %s seconds and try again.." % config.interval)
					sleep(config.interval)
				else:
					log.error("No more messages from server. Exiting...")
					return
