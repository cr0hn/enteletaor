# -*- coding: utf-8 -*-


"""
This file contains monkey patches for
"""

from __future__ import absolute_import


def new_transport_init(self, host, connect_timeout):

	import errno
	import re
	import socket
	import ssl

	# Jython does not have this attribute
	try:
		from socket import SOL_TCP
	except ImportError:  # pragma: no cover
		from socket import IPPROTO_TCP as SOL_TCP  # noqa

	try:
		from ssl import SSLError
	except ImportError:
		class SSLError(Exception):  # noqa
			pass

	from struct import pack, unpack

	from amqp.exceptions import UnexpectedFrame
	from amqp.utils import get_errno, set_cloexec

	_UNAVAIL = errno.EAGAIN, errno.EINTR, errno.ENOENT

	AMQP_PORT = 5672

	EMPTY_BUFFER = bytes()

	# Yes, Advanced Message Queuing Protocol Protocol is redundant
	AMQP_PROTOCOL_HEADER = 'AMQP\x01\x01\x00\x09'.encode('latin_1')

	# Match things like: [fe80::1]:5432, from RFC 2732
	IPV6_LITERAL = re.compile(r'\[([\.0-9a-f:]+)\](?::(\d+))?')

	# --------------------------------------------------------------------------
	# __init__ content:
	# --------------------------------------------------------------------------
	self.connected = True
	msg = None
	port = AMQP_PORT

	m = IPV6_LITERAL.match(host)
	if m:
		host = m.group(1)
		if m.group(2):
			port = int(m.group(2))
	else:
		if ':' in host:
			host, port = host.rsplit(':', 1)
			port = int(port)

	self.sock = None
	last_err = None
	for res in socket.getaddrinfo(host, port, 0,
	                              socket.SOCK_STREAM, SOL_TCP):
		af, socktype, proto, canonname, sa = res
		try:
			self.sock = socket.socket(af, socktype, proto)
			try:
				set_cloexec(self.sock, True)
			except NotImplementedError:
				pass
			self.sock.settimeout(connect_timeout)
			self.sock.connect(sa)
		except socket.error as exc:
			msg = exc
			self.sock.close()
			self.sock = None
			last_err = msg
			continue
		break

	if not self.sock:
		# Didn't connect, return the most recent error message
		raise socket.error(last_err)

	try:
		# self.sock.settimeout(None)
		self.sock.setsockopt(SOL_TCP, socket.TCP_NODELAY, 1)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

		self._setup_transport()

		self._write(AMQP_PROTOCOL_HEADER)
	except (OSError, IOError, socket.error) as exc:
		if get_errno(exc) not in _UNAVAIL:
			self.connected = False
		raise


# --------------------------------------------------------------------------
# amqlib
# --------------------------------------------------------------------------
def patch_transport():
	"""
	This function path transport constructor to fix timeout in sockets
	"""

	from amqp.transport import _AbstractTransport

	_AbstractTransport.__init__ = new_transport_init
