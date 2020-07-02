
Pattoo Operating System Autonomous Agent
========================================

``pattoo_agent_os_autonomousd`` gathers performance data from the operating system on which it is running and reports it to the ``pattoo`` server.

The ``pattoo_agent_os_autonomousd`` has a number of advantages over using a combination of ``pattoo_agent_os_hubd`` and ``pattoo_agent_os_spoked``.

#. ``pattoo_agent_os_autonomousd`` can the used where the remote client is allowed to initiate connections to the ``pattoo`` server, but not vice versa.
#. Many more ``pattoo_agent_os_autonomousd`` clients can be supported as the central ``pattoo_agent_os_hubd`` daemon can get overloaded if it needs to poll a large number of remote devices.

If this describes your needs, then continue reading!

Installation
------------

These steps outline what needs to be done to get ``pattoo_agent_os_autonomousd`` working.

#. Follow the installation steps in the :doc:`installation` file.
#. Configure the ``pattoo.yaml`` configuration file following the steps in :doc:`configuration`. This file tells ``pattoo_agent_os_autonomousd``, and all other agents, how to communicate with the ``pattoo`` server.
#. Create a ``pattoo_agent_os_autonomousd.yaml`` configuration file. Details on how to do this follow.
#. Start the desired daemons using the commands below. You may want to make these ``systemd`` daemons, if so follow the steps in the :doc:`installation` file.

Setting the  Configuration Directory Location
---------------------------------------------

``pattoo_agent_os_autonomousd`` is a standard ``pattoo`` agent and needs its configuration directory defined by using the ``PATTOO_CONFIGDIR`` environmental variable. Here is how to do this from the Linux command line:

.. code-block:: bash

   $ export PATTOO_CONFIGDIR=/path/to/configuration/directory

``pattoo_agent_os_autonomousd`` client will read its own ``pattoo_agent_os_autonomousd.yaml`` configuration file located this directory when ``PATTOO_CONFIGDIR`` is set.

You can automatically set this variable each time you log in by adding these lines to your ``~/.bash_profile`` file.

.. code-block:: bash

   export PATTOO_CONFIGDIR=/path/to/configuration/directory

Make sure that files in this directory are readable by the user that will be running standard ``pattoo`` agent daemons or scripts.


Configuring ``pattoo_agent_os_autonomousd.yaml``
------------------------------------------------

Let's get started on configuring ``pattoo_agent_os_autonomousd.yaml``.

``pattoo_agent_os_autonomousd`` Section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here is a sample of what should be added. An explanation follows.

**NOTE:** The indentations in the YAML configuration are important. Make sure indentations line up. Dashes '-' indicate one item in a list of items.

.. code-block:: yaml

    pattoo_agent_os_autonomousd:

        polling_interval: 300

Configuration Explanation
~~~~~~~~~~~~~~~~~~~~~~~~~

This table outlines the purpose of each configuration parameter

.. list-table::
   :header-rows: 1

   * - Section
     - Sub-Section
     - Config Options
     - Description
   * - ``pattoo_agent_os_autonomousd``
     -
     -
     -
   * -
     - ``polling_interval``
     -
     - The ``pattoo_agent_os_autonomousd`` will report to the ``pattoo`` server every ``polling_interval`` seconds


Polling
-------

Use ``pattoo_agent_os_autonomousd`` to poll your devices. The daemon has a simple command structure below.

You will need a ``pattoo_agent_os_autonomousd.yaml`` configuration file in the ``PATTOO_CONFIGDIR`` directory before you start.

.. code-block:: bash

   $ bin/pattoo_agent_os_autonomousd.py --help
   usage: pattoo_agent_os_autonomousd.py [-h] [--start] [--stop] [--status] [--restart]
                            [--force]

   optional arguments:
     -h, --help  show this help message and exit
     --start     Start the agent daemon.
     --stop      Stop the agent daemon.
     --status    Get daemon daemon status.
     --restart   Restart the agent daemon.
     --force     Stops or restarts the agent daemon ungracefully when used with --stop or
                 --restart.
   $

General Operation
^^^^^^^^^^^^^^^^^
Use these commands for general operation of the daemon.

Starting
~~~~~~~~
Start the daemon using this command.

.. code-block:: bash

  $ bin/pattoo_agent_os_autonomousd.py --start

Stopping
~~~~~~~~
Stop the daemon using this command.

.. code-block:: bash

    $ bin/pattoo_agent_os_autonomousd.py --stop


Restarting
~~~~~~~~~~
Restart the daemon using this command.

.. code-block:: bash

    $ bin/pattoo_agent_os_autonomousd.py --restart


Start Polling at Boot
^^^^^^^^^^^^^^^^^^^^^

:doc:`configuration` provides information on how to get the ``pattoo_agent_os_autonomousd`` daemon to start at boot.

Troubleshooting
---------------

Troubleshooting steps can be found in the `PattooShared troubleshooting documentation <https://pattoo-shared.readthedocs.io/en/latest/troubleshooting.html>`_
