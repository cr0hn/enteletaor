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
