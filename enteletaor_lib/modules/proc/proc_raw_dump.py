# -*- coding: utf-8 -*-

import six
import logging

from time import sleep
from kombu import Connection

from .utils import list_remote_process

log = logging.getLogger()


# ----------------------------------------------------------------------
def action_proc_raw_dump(config):

	log.warning("  - Trying to connect with server...")

	url = '%s://%s' % (config.broker_type, config.target)

	# with Connection('redis://%s' % REDIS) as conn:
	with Connection(url) as conn:
		in_queue = conn.SimpleQueue('celery')

		while 1:

			for remote_process, remote_args in list_remote_process(config, in_queue):
				# Show info
				log.error("Found process information:")
				log.error("  -  Remote process name: '%s'" % remote_process)
				log.error("  -  Input parameters:")

				for i, x in enumerate(remote_args):
					log.error("      -> P%s: %s" % (i, x))

			# Queue is empty -> wait
			if config.streaming_mode:
				log.error("No more messages from server. Waiting for %s seconds and try again.." % config.interval)
				sleep(config.interval)
			else:
				log.error("No more messages from server. Exiting...")
				return
