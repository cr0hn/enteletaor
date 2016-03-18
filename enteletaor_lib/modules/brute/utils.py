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
import socket
import logging

from .patch import patch_transport
from .exceptions import AuthRequired
from .authers import brute_amqp, brute_redis, brute_zmq

# Monkey patch for AMQP lib
patch_transport()

log = logging.getLogger()


# ----------------------------------------------------------------------
def is_rabbit(host, port, user, password, config):
	"""
	Custom detection of RabbitMQ servers
	"""
	s = socket.socket()
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.connect((host, int(port)))
	s.send(b"A\r\n\r\n\r\n\r\n\r\n\r\n")
	data = (s.recv(1000000))

	if b"AMQP" in data:
		# Oks, its a RabbitMQ!
		try:
			brute_amqp(host, port, user, password)

			return True
		except socket.timeout:
			raise AuthRequired()
	else:
		return False


# ----------------------------------------------------------------------
def get_server_type(config):
	"""
	Get server type and if it's open or closed.

	Returns server type and their status as format: (TYPE, STATUS, port), where:

	- TYPE: redis/zeromq/amqp
	- STATUS: open/closed/auth
	
	:return: type of server as format: (type, status, port)
	:rtype: (str, str, int)
	"""
	handlers = {
		'Redis': brute_redis,
		'RabbitMQ': is_rabbit,
		'ZeroMQ': brute_zmq
	}

	host = config.target
	port = config.port
	user = config.user
	password = None
	result = -1

	log.warning("    > Analyzing host '%s' with port '%s' " % (host, port))

	try:

		# Try to check if port is open
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(config.timeout)

		result = s.connect_ex((host, int(port)))

	except socket.gaierror as e:
		log.debug("%s error: %s" % (port, e))
	finally:
		s.close()

	# Is port open?
	if result == 0:
		log.info("         <i> Port '%s' is open in '%s'" % (port, host))

		# Check each serve
		for server_type, handle in six.iteritems(handlers):

			try:
				if handle(host, port, user, password, config) is True:
					return server_type, "open", port

			except AuthRequired:
				return server_type, "auth", port
	else:
		return None, "closed", port
