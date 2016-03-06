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
import csv
import logging

from time import sleep
from kombu import Connection

from .utils import list_remote_process

log = logging.getLogger()


# ----------------------------------------------------------------------
def action_proc_raw_dump(config):

	log.warning("  - Trying to connect with server...")

	url = '%s://%s' % (config.broker_type, config.target)

	f_output = None
	csv_output = None

	if config.output is not None:
		fixed_f = "%s.csv" % config.output if ".csv" not in config.output else config.output

		f_output = open(fixed_f, "a")
		csv_output = csv.writer(f_output)

		log.error("  - Storing results at '%s'" % fixed_f)

		# Write first col
		csv_output.writerow([
			"# Task name",
			"Parameters (position#value)"
		])

	already_processed = set()

	# with Connection('redis://%s' % REDIS) as conn:
	with Connection(url) as conn:
		in_queue = conn.SimpleQueue('celery')

		while 1:

			for remote_task, remote_args, task_id in list_remote_process(config, in_queue):

				# Task already processed?
				if task_id not in already_processed:

					# Track
					already_processed.add(task_id)

					# Show info
					log.error("  Found process information:")
					log.error("  -  Remote tasks name: '%s'" % remote_task)
					log.error("  -  Input parameters:")

					to_csv = [remote_task]

					for i, x in enumerate(remote_args):
						log.error("      -> P%s: %s" % (i, x))

						# Prepare to store JSON
						to_csv.append("%s#%s" % (i, x))

					# Store
					if csv_output is not None:
						csv_output.writerow(to_csv)

			# Queue is empty -> wait
			if config.streaming_mode:
				log.error("  -> No more messages from server. Waiting for %s seconds and try again.." % config.interval)
				sleep(config.interval)
			else:
				log.error("  -> No more messages from server. Exiting...")
				return

	# Close file descriptor
	if f_output is not None:
		f_output.close()
		csv_output.close()
