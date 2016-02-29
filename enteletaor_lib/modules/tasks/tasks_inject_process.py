# -*- coding: utf-8 -*-


import six
import uuid
import json
import logging

from kombu import Connection
from collections import OrderedDict


log = logging.getLogger()


# ----------------------------------------------------------------------
def action_task_inject_process(config):

	if config.function_files is None:
		log.error("  - input .json file with process files is needed")
		return

	# --------------------------------------------------------------------------
	# Load process information
	# --------------------------------------------------------------------------
	with open(config.function_files, "r") as f:
		f_info = json.load(f)

	log.error("  - Building process...")

	# Search and inject process
	injections = []
	for p in f_info:

		parameters = OrderedDict({x["param_position"]: x["param_value"] for x in p['parameters']})

		# --------------------------------------------------------------------------
		# Fill process information
		# --------------------------------------------------------------------------
		inject_process = {
			"args": [y for x, y in six.iteritems(parameters)],
			"callbacks": None,
			"chord": None,
			"errbacks": None,
			"eta": None,
			"expires": None,
			"id": uuid.uuid1(),
			"kwargs": {},
			"retries": 0,
			"task": p["function"],
			"taskset": None,
			"timelimit": [
				None,
				None
			],
			"utc": True
		}

		injections.append(inject_process)

	# --------------------------------------------------------------------------
	# Re-inject messages
	# --------------------------------------------------------------------------
	log.warning("  - Trying to connect with server...")

	url = '%s://%s' % (config.broker_type, config.target)

	with Connection(url) as conn:
		in_queue = conn.SimpleQueue('celery')

		log.error("  - Sending processes to '%s'" % config.target)

		for i, e in enumerate(injections, 1):
			log.warning("      %s) %s" % (i, e['task']))
			# pass
			in_queue.put(e, serializer="pickle")
