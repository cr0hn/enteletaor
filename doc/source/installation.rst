Installation
============

Dependencies
------------

First you be sure you have installed this packages:

For Python 2 & 3
++++++++++++++++

.. code-block:: bash

    # sudo apt-get install -y libzmq3 libzmq3-dev

Python 3 only (recommended)
+++++++++++++++++++++++++++

.. code-block:: bash

    # sudo apt-get install -y python3-pip

Python 2 only
+++++++++++++

.. code-block:: bash

    # sudo apt-get install -y python2.7-dev


Installation from PIP (recommended)
-----------------------------------

The easiest way to install enteleteaor is from Pypi. To do this, only run:

Python 2
++++++++

.. code-block:: bash

    # python -m pip install enteletaor

Python 3
++++++++

.. code-block:: bash

    # python3 -m pip install enteletaor

Then run enteleteaor writing:

.. code-block:: bash

    # enteleteaor -h

or, in Python 3:

.. code-block:: bash

    # enteleteaor3 -h

.. note::

    Remember that, if you install enteleteaor in **Python 3** executable will be called **enteletaor3** -> ending in **3**.

    If you install in **Python 2** executable will be **enteletaor**, without 3.

Installation from source
------------------------

Also, you can download source code from github using git:

.. code-block:: bash

    git clone https://github.com/cr0hn/enteleteaor.git enteleteaor

Next you need to install dependencies from ``requirements.txt``:

.. code-block:: bash

    pip install -r requirements.txt

.. note::

   If you're not running enteleteaor in a virtualenv, probably you need to be root to install requirements. So, you can use ``sudo`` command.

Finally you can run enteleteaor:

.. code-block:: bash

    # cd enteleteaor_lib
    # python enteleteaor.py -h

