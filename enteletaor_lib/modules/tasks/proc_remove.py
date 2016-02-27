# -*- coding: utf-8 -*-

import logging

from kombu import Connection

from .utils import get_remote_messages

log = logging.getLogger()


# ----------------------------------------------------------------------
def action_proc_remove(config):

	log.warning("  - Trying to connect with server...")

	url = '%s://%s' % (config.broker_type, config.target)

	with Connection(url) as conn:
		in_queue = conn.SimpleQueue('celery')

		# Get remote process
		for _ in get_remote_messages(config, in_queue, False):
			pass

		log.error("   - All processes removed from '%s'" % config.target)
