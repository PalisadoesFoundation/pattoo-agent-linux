
Pattoo Hub and Spoke Operating System Agents
============================================

The ``pattoo_agent_os_hubd`` and ``pattoo_agent_os_spoked`` daemons operate together to report on system performance.

#. The ``pattoo_agent_os_spoked`` runs on a remote server where it provides system performance data on a simple web page.
#. The ``pattoo_agent_os_hubd`` polls one or more ``pattoo_agent_os_spoked`` enabled devices for data and reports this to the ``pattoo`` server.

Installation
------------

These steps outline what needs to be done to get ``pattoo_agent_os_hubd`` and ``pattoo_agent_os_spoked`` working.

#. Follow the installation steps in the :doc:`installation` file.
#. Configure the ``pattoo.yaml`` configuration file following the steps in :doc:`configuration`. This file tells ``pattoo_agent_os_hubd`` and ``pattoo_agent_os_spoked``, and all other agents, how to communicate with the ``pattoo`` server.
#. Create a ``pattoo_agent_os_hubd.yaml`` and a  ``pattoo_agent_os_spoked.yaml`` configuration file to manage each daemon. Details on how to do this follow.
#. Start the desired daemons as explained in sections to follow. You may want to make these ``systemd`` daemons, if so follow the steps in the :doc:`installation` file.


Setting the  Configuration Directory Location
---------------------------------------------

``pattoo_agent_os_hubd`` and ``pattoo_agent_os_spoked`` are standard ``pattoo`` agent and need their configuration directory defined by using the ``PATTOO_CONFIGDIR`` environmental variable. Here is how to do this from the Linux command line:

.. code-block:: bash

   $ export PATTOO_CONFIGDIR=/path/to/configuration/directory

``pattoo_agent_os_hubd`` and ``pattoo_agent_os_spoked`` clients will read respective ``pattoo_agent_os_hubd.yaml`` and ``pattoo_agent_os_spoked.yaml`` configuration files located this directory when ``PATTOO_CONFIGDIR`` is set.

You can automatically set this variable each time you log in by adding these lines to your ``~/.bash_profile`` file.

.. code-block:: bash

   export PATTOO_CONFIGDIR=/path/to/configuration/directory

Make sure that files in this directory are readable by the user that will be running standard ``pattoo`` agent daemons or scripts.


Configuring the Hub Daemon
---------------------------------

The ``pattoo_agent_os_spoked`` is configured using the ``pattoo_agent_os_spoked.yaml`` file. Let's see how it is done.


pattoo_agent_os_spoked Section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here is a sample of what should be added. An explanation follows.

**NOTE:** The indentations in the YAML configuration are important. Make sure indentations line up. Dashes '-' indicate one item in a list of items.

.. code-block:: yaml

   pattoo_agent_os_spoked:
       ip_listen_address: 0.0.0.0
       ip_bind_port: 5000

Configuration Explanation
~~~~~~~~~~~~~~~~~~~~~~~~~

This table outlines the purpose of each configuration parameter

.. list-table::
   :header-rows: 1

   * - Section
     - Config Options
     - Description
   * - ``pattoo_agent_os_spoked``
     -
     - **Note:** Only required for devices running ``pattoo_agent_os_spoked``
   * -
     - ``ip_listen_address``
     - IP address on which the API server will listen. Setting this to ``0.0.0.0`` will make it listen on all IPv4 addresses. Setting to ``"0::"`` will make it listen on all IPv6 configured interfaces. It will not listen on IPv4 and IPv6 addresses simultaneously. You must **quote** all IPv6 addresses. The default value is ``0.0.0.0``
   * -
     - ``ip_bind_port``
     - TCP port on which the API will listen

Operating the Spoke Daemon
------------------------------

The ``pattoo_agent_os_spoked`` creates a web page on the device it runs to report on the device's operating status.

You will need a ``pattoo_agent_os_spoked.yaml`` configuration file in the ``PATTOO_CONFIGDIR`` directory before you start.

.. code-block:: bash

   $ bin/pattoo_agent_os_spoked.py --help
   usage: pattoo_agent_os_spoked.py [-h] [--start] [--stop] [--status] [--restart]
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

  $ bin/pattoo_agent_os_spoked.py --start

Stopping
~~~~~~~~
Stop the daemon using this command.

.. code-block:: bash

    $ bin/pattoo_agent_os_spoked.py --stop


Restarting
~~~~~~~~~~
Restart the daemon using this command.

.. code-block:: bash

    $ bin/pattoo_agent_os_spoked.py --restart


Start Polling at Boot
^^^^^^^^^^^^^^^^^^^^^

:doc:`configuration` provides information on how to get the ``pattoo_agent_os_spoked`` daemon to start at boot.


Testing
^^^^^^^

If you are running ``pattoo_agent_os_spoked`` on your local system, then you can test it by pointing your browser to ``http://localhost:5000/pattoo-agent-os/300`` to view the system data. In this case ``300`` is a reference to the polling interval of the polling device. On  a Linux system you should be able to see the results by using this command ``curl http://localhost:5000/pattoo-agent-os/300 | json_pp`` or  ``curl http://localhost:5000/pattoo-agent-os/300`` if you don't have JSON Pretty Print installed.



Configuring the ``Hub`` Daemon
------------------------------

The ``pattoo_agent_os_hubd`` is configured using the ``pattoo_agent_os_hubd.yaml`` file. Let's see how it is done.

pattoo_agent_os_hubd Section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here is a sample of what should be added. An explanation follows.

**NOTE:** The indentations in the YAML configuration are important. Make sure indentations line up. Dashes '-' indicate one item in a list of items.

.. code-block:: yaml

   pattoo_agent_os_hubd:
       ip_devices:
         - ip_address: 127.0.0.1
           ip_bind_port: 5000
         - ip_address: 127.0.0.2
           ip_bind_port: 5000

Configuration Explanation
~~~~~~~~~~~~~~~~~~~~~~~~~

This table outlines the purpose of each configuration parameter

.. list-table::
  :header-rows: 1

  * - Section
    - Sub-Section
    - Config Options
    - Description
  * - ``pattoo_agent_os_hubd``
    -
    -
    - **Note:** Only required for devices running ``pattoo_agent_os_hubd``
  * -
    - ``ip_devices``
    -
    - Sub-Section providing a list of IP addresses or hostnames running ``pattoo_agent_os_spoked`` that need to be polled for data. You must specify an ``ip_address`` and TCP ``ip_bind_port``\ for each of these devices.
  * -
    -
    - ``ip_address``
    - The IP adrress of the remote ``ip_device``.
  * -
    -
    - ``bind_port``
    - The TCP port on which the remote ``ip_device`` is listening.

Polling From Hubs to Spokes
---------------------------

Use ``pattoo_agent_os_hubd`` to poll your devices. The daemon has a simple command structure below.

You will need a ``pattoo_agent_os_hubd.yaml`` configuration file in the ``PATTOO_CONFIGDIR`` directory before you start.

.. code-block:: bash

   $ bin/pattoo_agent_os_hubd.py --help
   usage: pattoo_agent_os_hubd.py [-h] [--start] [--stop] [--status] [--restart]
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

  $ bin/pattoo_agent_os_hubd.py --start

Stopping
~~~~~~~~
Stop the daemon using this command.

.. code-block:: bash

    $ bin/pattoo_agent_os_hubd.py --stop


Restarting
~~~~~~~~~~
Restart the daemon using this command.

.. code-block:: bash

    $ bin/pattoo_agent_os_hubd.py --restart


Start Polling at Boot
^^^^^^^^^^^^^^^^^^^^^

:doc:`configuration` provides information on how to get the ``pattoo_agent_os_hubd`` daemon to start at boot.

Troubleshooting
---------------

Troubleshooting steps can be found in the `PattooShared troubleshooting documentation <https://pattoo-shared.readthedocs.io/en/latest/troubleshooting.html>`_
