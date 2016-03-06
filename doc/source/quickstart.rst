Quick Start
===========

Enteleteaor have 3 super commands available:

 - scan: Discover open brokers.
 - tasks: handle remote tasks.
 - redis: specific actions for Redis server.

This document contains an overview of enteleteaor with some examples for each super commands. If you want learn more visit the :doc:`advanced`.

Python versions
---------------

Enteleteaor can run in Python 2.7.x and 3.x. Python 3 is recommended, but you can use python 2.7 without problem.

Getting help
------------

Super commands ``tasks`` and ``redis`` has many sub-options, you can get help using ``-h`` in each super command:

.. code-block:: bash
    :linenos:
    :emphasize-lines: 9-14

    # enteleteaor scan -h
    usage: enteletaor.py redis [-h]
                           {info,disconnect,dump,cache,discover-dbs,connected}
                           ...

    positional arguments:
      {info,disconnect,dump,cache,discover-dbs,connected}
                            redis commands:
        info                open a remote shell through the Redis server
        disconnect          disconnect one or all users from Redis server
        dump                dumps all keys in Redis database
        cache               poison remotes cache using Redis server
        discover-dbs        discover all Redis DBs at server
        connected           get connected users to Redis server

    optional arguments:
      -h, --help            show this help message and exit


Setting verbosity level
-----------------------

Enteleteaor has 5 verbosity levels. You can modify level adding ``-v`` to command line:

.. code-block:: bash

    # enteleteaor -v scan -t 10.10.0.10
    # enteleteaor -vvvv scan -t 10.10.0.10

.. note::

    Be careful to put ``-v`` between enteleteaor and top action:

    - enteleteaor -vv scan ... -> **GOOD**
    - enteleteaor scan -vv ... -> **BAD**

Quick scan
----------

You can try to discover if some host has open brokers running running:

.. code-block:: bash

    # enteleteaor -v scan -t 10.10.0.10
    [ * ] Starting Enteletaor execution
    [ * ]   - Number of targets to analyze: 1
    [ * ]   - Starting scan
    [ * ]     > Analyzing host '10.10.0.10'
    [ * ]       <!!> Open 'RabbitMQ' server found in port '5672' at '10.10.0.10'
    [ * ]       <!!> Open 'Redis' server found in port '6379' at '10.10.0.10'
    [ * ]       <!!> Open 'ZeroMQ' server found in port '5555' at '10.10.0.10'
    [ * ]   - Open services found:
    [ * ]     -> Host - 10.10.0.10
    [ * ]        * 6379/TCP [Redis]
    [ * ]        * 5672/TCP [RabbitMQ]
    [ * ]        * 5555/TCP [ZeroMQ]
    [ * ] Done!

Also we can analyze an entire network:

.. code-block:: bash

    # enteleteaor scan -t 10.10.0.10/24


Remote tasks
------------

Listing remote tasks
++++++++++++++++++++

With enteleteaor you can handle remote tasks, for example, you can list pending tasks doing:

.. code-block:: bash

    # enteleteaor -v tasks list-tasks -t 10.10.0.10
    [ * ] Starting Enteletaor execution
    [ * ]   - Remote process found:
    [ * ]      -> tasks.send_mail (param_0:str, param_1:str, param_2:str)
    [ * ] Done!

Enteleteaor is telling us that it has discovered a task, called ``tasks.send_mail`` with 3 parameters, and the type of parameter by their position.

.. note::

    The tool can't discover the parameter name, thus indicate the position.

This task can match with this programing function, i.e:

.. code-block:: python
    :linenos:
    :emphasize-lines: 3,6,9

    def send_mail(to, from, message):
        """
        :param to: mail destination
        :type to: str

        :param from: mail sender
        :type from: str

        :param message: content of message
        :type message: str
        """
        # Code that send the e-mail

Dumping tasks content
+++++++++++++++++++++

Enteleteaor not only permit us listing remote tasks, it also can dump their content:

.. code-block:: bash
    :linenos:
    :emphasize-lines: 6-8,12-14,18-20

    # enteleteaor tasks raw-dump -t 10.10.0.10
    [ * ] Starting Enteletaor execution
    [ * ]   Found process information:
    [ * ]   -  Remote process name: 'tasks.send_mail'
    [ * ]   -  Input parameters:
    [ * ]       -> P0: particia@stephnie.com
    [ * ]       -> P1: Open This Email The broke girl's guide to a luxury vacation What Can You Afford?
    [ * ]       -> P2: Asia and the Pacific and was already at war with the invasion of the United States emerged as rival superpowers, setting the stage for the Cold War, which lasted for the next 46 years.
    [ * ]   Found process information:
    [ * ]   -  Remote process name: 'tasks.send_mail'
    [ * ]   -  Input parameters:
    [ * ]       -> P0: eveline@stephnie.com
    [ * ]       -> P1: Can You Afford?
    [ * ]       -> P2: Berlin by Soviet and Polish troops and the coalition of the United Kingdom and the United States and European territories in the Pacific, the Axis lost the initiative and undertook strategic retreat on all fronts.
    [ * ]   Found process information:
    [ * ]   -  Remote process name: 'tasks.send_mail'
    [ * ]   -  Input parameters:
    [ * ]       -> P0: milford@stephnie.com
    [ * ]       -> P1: Hey Don't Open This Email The broke girl's guide to a luxury vacation What Can You Afford?
    [ * ]       -> P2: European neighbours, Poland, Finland, Romania and the Axis.
    [ * ] No more messages from server. Exiting...
    [ * ] Done!

Redis
-----

Redis is a powerful software, with many options, so it has a specific super command.

Getting remove Redis info
+++++++++++++++++++++++++

If you want list remote Redis server information, only type:

.. code-block:: bash

    # enteleteaor redis info -t 10.10.0.10
    [ * ] Starting Enteletaor execution
    [ * ] Config for server '10.10.0.10':
    [ * ]   - appendonly: no
    [ * ]   - auto-aof-rewrite-min-size: 67108864
     ...
    [ * ]   - timeout: 0
    [ * ]   - databases: 16
    [ * ]   - slave-priority: 100
    [ * ]   - dir: /var/lib/redis
    [ * ] Done!

Listing users
+++++++++++++

We can also list all connected users to Redis server. A user could be a web application (that uses Redis as cache), a monitoring system or, even, the administrator.

.. code-block:: bash

    # enteleteaor redis connected -t 10.10.0.10
    [ * ] Starting Enteletaor execution
    [ * ] Connected users to '10.10.0.10':
    [ * ]   - 10.10.0.2:52748 (DB: 0)
    [ * ]   - 10.10.0.2:52749 (DB: 0)
    [ * ]   - 10.10.0.2:52752 (DB: 0)
    [ * ]   - 127.0.0.1:42262 (DB: 0)
    [ * ]   - 10.10.0.2:53095 (DB: 0)
    [ * ] Done!

Localhost addresses usually is a local monitoring system or admin.