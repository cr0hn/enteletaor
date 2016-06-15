.. Documentation master file, created by
   sphinx-quickstart on Wed Feb 11 01:21:33 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Enteletaor documentation!
====================================

.. figure:: ../images/enteletaor-logo-150px.png
   :align: left

Enteletaor is a message Queue & Broker Injection tool.

+----------------+------------------------------------+
|Project site    | http://github.com/cr0hn/enteletaor |
+----------------+------------------------------------+
|Documentation   | http://enteletaor.readthedocs.org  |
+----------------+------------------------------------+
|Author          | Daniel Garcia (cr0hn) - @ggdaniel  |
+----------------+------------------------------------+
|Last Version    | 1.0.0                              |
+----------------+------------------------------------+
|Python versions | 2.7.x % 3.x                        |
+----------------+------------------------------------+

Quick project description
-------------------------

Enteletaor is a tool that can handle information from open brokers.

Some of the actions you can do:

   - Listing remote tasks.
   - Read remote task content.
   - Disconnect remote clients from Redis server (even the admin!)
   - Inject tasks into remote processes.
   - Make a scan to discover open brokers.

Currently supported brokers are:

   - RabbitMQ (or AMQP compatible).
   - ZeroMQ.
   - Redis.


Content Index
-------------

.. toctree::
   :maxdepth: 3

   installation
   quickstart
   advanced


Licence
-------

I believe in freedom, so Enteletaor is released under BSD license.
