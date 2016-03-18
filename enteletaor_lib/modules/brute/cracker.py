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
import logging
import threading

import eventlet

from eventlet import tpool

from .authers import brute_redis, brute_amqp, brute_zmq
from .exceptions import AuthRequired

FOUND = None
THREADS = []

log = logging.getLogger()

# Path thread library
eventlet.monkey_patch(socket=True, select=True, thread=True)


# ----------------------------------------------------------------------
class FoundPassword(Exception):
	pass


# ----------------------------------------------------------------------
# Runners
# ----------------------------------------------------------------------
def find_password_sem(fn, sem, host, port, user, password, db):
	global FOUND

	try:
		if fn(host, port, user, password, None) is True:
			FOUND = "%s: %s%s" % (host, "", password)
	except AuthRequired:
		pass

	sem.release()


# ----------------------------------------------------------------------
def find_password(fn, host, port, user, password, db):
	global FOUND

	try:
		if fn(host, port, user, password, db) is True:
			FOUND = "%s - %s%s" % (host, "%s/" % user, password)
	except AuthRequired:
		pass


# ----------------------------------------------------------------------
# Workers function
# ----------------------------------------------------------------------
def cracking_threads(fn, port, config):
	global FOUND
	global THREADS

	th = []
	sem = threading.BoundedSemaphore(config.concurrency)

	with open(config.wordlist, "r") as f:
		for i, password in enumerate(f.readlines()):
			password = password.replace("\n", "")

			# log.debug("       -- Testing '%s'" % password)

			if FOUND is not None:
				break

			# Launch password
			t = threading.Thread(target=find_password_sem, args=(fn, sem, config.target, port, config.user, password, None, ))

			th.append(t)

			sem.acquire()
			t.start()

			if (i % 500) == 0:
				log.info("    >> %s passwords tested" % i)

	# Wait for ending
	for x in th:
		x.join()

	if FOUND is not None:
		log.error("  - Password found: %s" % FOUND)


# ----------------------------------------------------------------------
def cracking_evenlets(fn, port, config):

	global FOUND

	os.getenv("EVENTLET_THREADPOOL_SIZE", config.concurrency)

	try:
		with open(config.wordlist, "r") as f:
			for i, password in enumerate(f.readlines()):
				password = password.replace("\n", "")

				log.debug("     >> Testing %s" % password)

				if FOUND is not None:
					break

				tpool.execute(find_password, fn, config.target, port, config.user, password, None)

				if (i % 500) == 0:
					log.info("    >> %s passwords tested" % i)

	except FoundPassword as e:
		log.error("  - Credentials found: %s" % e)


# ----------------------------------------------------------------------
def cracking(server_type, port, config):

	crackers = {
		'redis': (brute_redis, cracking_evenlets),
		'rabbitmq': (brute_amqp, cracking_threads),
		'zeromq': (brute_zmq, cracking_evenlets)
	}

	mode, fn = crackers[server_type.lower()]

	# --------------------------------------------------------------------------
	# Check requisites
	# --------------------------------------------------------------------------
	if server_type.lower() == "rabbitmq":
		if config.user is None:
			log.error("  - Username is required for this server.")
			return

	fn(mode, port, config)
