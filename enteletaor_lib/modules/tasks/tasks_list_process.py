# -*- coding: utf-8 -*-
#
# Enteletaor - https://github.com/cr0hn/enteletaor
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the
# following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

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
			export_path = os.path.abspath(config.template)

			if ".json" not in export_path:
				export_path += ".json"

			# dumps
			json.dump(export_data, open(export_path, "w"))

			log.error("  - Template saved at: '%s'" % export_path)
