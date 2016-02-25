# -*- coding: utf-8 -*-

import six
import zmq
import json
import redis
import socket
import logging
import eventlet
import ipaddress
import amqp.connection


from functools import partial
from collections import defaultdict
from threading import Thread, BoundedSemaphore

from .patch import patch_transport
from enteletaor_lib.libs.contrib.inetnum import get_inet_num

# Monkey patch for AMQP lib
patch_transport()
# Path thread library
eventlet.monkey_patch(socket=True, select=True, thread=True)


# Reconfigure AMQP LOGGER
logging.getLogger('amqp').setLevel(100)

log = logging.getLogger()

OPEN_SERVICES = defaultdict(dict)


# ----------------------------------------------------------------------
def _do_scan(config, sem, host):
	"""
	This function try to find brokers services open in remote servers
	"""

	handlers = {
		'Redis': handle_redis,
		'RabbitMQ': handle_amqp,
		'ZeroMQ': handle_zmq
	}

	log.warning("    > Analyzing host '%s' " % host)

	for port in config.ports.split(","):

		# Check each serve
		for server_type, handle in six.iteritems(handlers):

			log.info("      >> Trying to find %s service in '%s' port '%s'." % (server_type, host, port))

			try:

				# Try to check if port is open
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.settimeout(config.timeout)

				result = s.connect_ex((host, int(port)))

			except socket.gaierror as e:
				log.debug("%s : %s error: %s" % (server_type, port, e))
				continue
			finally:
				s.close()

			# Is port open?
			if result == 0:
				log.info("         <i> Port '%s' is open in '%s'" % (port, host))

				if handle(host, port, config) is True:
					log.error("      <!!> Open '%s' server found in port '%s' at '%s'" % (server_type, port, host))

					OPEN_SERVICES[host][server_type] = dict(
						state="open",
						port=port
					)
			else:
				log.debug("        <i> Port %s is closed" % port)

	sem.release()


# ----------------------------------------------------------------------
def action_scan_main(config):
	# --------------------------------------------------------------------------
	# Resolve target
	# --------------------------------------------------------------------------
	all_ips = build_targets(config)

	# --------------------------------------------------------------------------
	# Preparing scan
	# --------------------------------------------------------------------------
	target_number = len(all_ips)

	log.warning("  - Number of targets to analyze: %s" % target_number)

	# Semaphore
	sem = BoundedSemaphore(config.concurrency)
	threads = []

	# Map parameters
	_fn = partial(_do_scan, config, sem)

	log.error("  - Starting scan")

	# --------------------------------------------------------------------------
	# Do scan
	# --------------------------------------------------------------------------
	for x in all_ips:
		sem.acquire()

		t = Thread(target=_fn, args=(x,))
		threads.append(t)

		t.start()

	for t in threads:
		t.join()

	# --------------------------------------------------------------------------
	# Display results
	# --------------------------------------------------------------------------
	if OPEN_SERVICES:
		log.error("  - Open services found:")
		for host, content in six.iteritems(OPEN_SERVICES):
			log.error("    -> Host - %s" % host)
			for server_type, server_info in six.iteritems(content):
				log.error("       * %s/TCP [%s]" % (server_info['port'], server_type))

	else:
		log.error("  - No open services found")

	# --------------------------------------------------------------------------
	# Export results
	# --------------------------------------------------------------------------
	if config.output is not None:
		_output_path = "%s.json" % config.output if ".json" not in config.output else config.output

		with open(_output_path, "w") as f:
			json.dump(OPEN_SERVICES, f)

		log.error("  - Output results saved into: %s" % _output_path)


# --------------------------------------------------------------------------
def build_targets(config):

	results = set()

	# Split targets
	for t in config.target.split(","):
		try:
			results.update(str(x) for x in ipaddress.ip_network(t, strict=False))
		except ValueError:
			# --------------------------------------------------------------------------
			# If reach this, is not a IPs, is a domain
			# --------------------------------------------------------------------------

			# Try to get all assigned IP of domain
			if config.own_ips is True:

				# Extract domain
				try:
					val = get_inet_num(t.split(".")[-2])

					if val is not None:

						for v in val:
							log.debug("  -> Detected registered network '%s'. Added for scan." % v)

							results.update(str(x) for x in ipaddress.ip_network(v, strict=False))
				except KeyError:
					# Invalid domain
					log.debug("    <ii> Error while try to extract domain: '%s'" % t)

			# --------------------------------------------------------------------------
			# Get all IPs for domain
			# --------------------------------------------------------------------------

			# If target is a domain, remove CDIR
			_target_cdir = t.split("/")

			_cleaned_target = _target_cdir[0]

			try:
				# Resolve
				host_ip = socket.gethostbyname(_cleaned_target)
			except socket.gaierror:
				# Try with the hostname with "www." again
				try:
					host_ip = socket.gethostbyname("www.%s" % _cleaned_target)
				except socket.gaierror:
					log.error("    <ii> Unable to resolve '%s'" % _cleaned_target)

					continue

			# Add CDIR to result
			scan_target = "%s%s" % (host_ip, "/%s" % _target_cdir[1] if len(_target_cdir) > 1 else "")

			results.update(str(x) for x in ipaddress.ip_network(scan_target, strict=False))

	return results


# --------------------------------------------------------------------------
# These 3 functions determinate if server has listen one of these services:
# - Redis server
# - RabbitMQ server
# - ZeroMQ PUB/SUB pattern
#
# Each function try to connect or do some action and determinate if service
# is on or not.
# --------------------------------------------------------------------------
def handle_redis(host, port=6379, extra_config=None):

	# log.debug("      * Connection to Redis: %s : %s" % (host, port))

	try:
		redis.StrictRedis(host=host, port=port, socket_connect_timeout=1, socket_timeout=1).config_get()

		return True

	except Exception:
		return False


# ----------------------------------------------------------------------
def handle_amqp(host, port=5672, extra_config=None):

	host_and_port = "%s:%s" % (host, port)

	# log.debug("      * Connection to RabbitMQ: %s : %s" % (host, port))

	try:
		amqp.connection.Connection(host=host_and_port,
		                           connect_timeout=1,
		                           read_timeout=1,
		                           socket_timeout=1)
		return True

	except Exception:
		return False


# ----------------------------------------------------------------------
def handle_zmq(host, port=5555, extra_config=None):

	# log.debug("      * Connection to ZeroMQ: %s : %s" % (host, port))

	context = zmq.Context()

	# Configure
	socket = context.socket(zmq.SUB)
	socket.setsockopt(zmq.SUBSCRIBE, b"")  # All topics
	socket.setsockopt(zmq.LINGER, 0)  # All topics
	socket.RCVTIMEO = 1000  # timeout: 1 sec

	# Connect
	socket.connect("tcp://%s:%s" % (host, port))

	# Try to receive
	try:
		socket.recv()

		return True
	except Exception:
		return False
	finally:
		socket.close()
