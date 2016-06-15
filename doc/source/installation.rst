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

The easiest way to install enteletaor is from Pypi. To do this, only run:

Python 2
++++++++

.. code-block:: bash

    # python -m pip install enteletaor

Python 3
++++++++

.. code-block:: bash

    # python3 -m pip install enteletaor

Then run enteletaor writing:

.. code-block:: bash

    # enteletaor -h

or, in Python 3:

.. code-block:: bash

    # enteletaor3 -h

.. note::

    Remember that, if you install enteletaor in **Python 3** executable will be called **enteletaor3** -> ending in **3**.

    If you install in **Python 2** executable will be **enteletaor**, without 3.

Installation from source
------------------------

Also, you can download source code from github using git:

.. code-block:: bash

    git clone https://github.com/cr0hn/enteletaor.git enteletaor

Next you need to install dependencies from ``requirements.txt``:

.. code-block:: bash

    pip install -r requirements.txt

.. note::

   If you're not running enteletaor in a virtualenv, probably you need to be root to install requirements. So, you can use ``sudo`` command.

Finally you can run enteletaor:

.. code-block:: bash

    # cd enteletaor_lib
    # python enteletaor.py -h

