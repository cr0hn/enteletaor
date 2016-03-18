# -*- coding: utf-8 -*-

import zmq
import redis
import socket
import redis.exceptions
import logging

import amqp.connection

from .exceptions import AuthRequired

log = logging.getLogger()


# --------------------------------------------------------------------------
# These 3 functions determinate if server has listen one of these services:
# - Redis server
# - RabbitMQ server
# - ZeroMQ PUB/SUB pattern
#
# Each function try to connect or do some action and determinate if service
# is on or not.
# --------------------------------------------------------------------------
def brute_redis(host, port=6379, user=None, password=None, db=0):

    try:
        redis.StrictRedis(host=host,
                          port=int(port),
                          socket_connect_timeout=1,
                          socket_timeout=1,
                          password=password,
                          db=db).ping()
        return True

    except redis.exceptions.ResponseError as e:
        if str(e).startswith("NOAUTH"):
            raise AuthRequired()
        else:
            return False
    except Exception:
        return False


# ----------------------------------------------------------------------
def brute_amqp(host, port=5672, user=None, password=None, db=0):

    host_and_port = "%s:%s" % (host, port)
    user_name = "guest" if user is None else user
    user_password = "guest" if password is None else password

    timeout = 0.2
    try:
        amqp.connection.Connection(host=host_and_port,
                                   userid=user_name,
                                   password=user_password,
                                   connect_timeout=timeout,
                                   read_timeout=timeout,
                                   socket_timeout=timeout).connected
        return True
    except socket.timeout as e:
        raise AuthRequired()
    except Exception:
        return False


# ----------------------------------------------------------------------
def brute_zmq(host, port=5555, user=None, password=None, db=0):

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
