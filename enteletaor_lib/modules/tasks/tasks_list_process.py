# -*- coding: utf-8 -*-

import os
import six
import json
import logging

from time import sleep
from kombu import Connection

from .utils import list_remote_process, get_param_type, export_process

log = logging.getLogger()


# ----------------------------------------------------------------------
def action_proc_list_tasks(config):

	log.warning("  - Trying to connect with server...")

	url = '%s://%s' % (config.broker_type, config.target)

	with Connection(url) as conn:

		in_queue = conn.SimpleQueue('celery')

		process_info = {}

		# Get remote process
		first_msg = True
		while 1:
			for remote_process, remote_args, _ in list_remote_process(config, in_queue):

				if remote_process not in process_info:
					process_info[remote_process] = remote_args

			if config.no_stream is False and not process_info:
				if first_msg is True:
					log.error("     -> Not messages found. Waiting ...")
					first_msg = False

				sleep(0.1)
			else:
				break

		# --------------------------------------------------------------------------
		# Try to identify parameters types
		# --------------------------------------------------------------------------

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

			export_data = export_process(process_info, config)

			# --------------------------------------------------------------------------
			# Save template
			# --------------------------------------------------------------------------
			# Build path in current dir
			export_path = "%s.json" % os.path.abspath(config.template)

			# dumps
			json.dump(export_data, open(export_path, "w"))

			log.error("  - Template saved at: '%s'" % export_path)
