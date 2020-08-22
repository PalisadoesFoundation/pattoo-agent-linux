###################
Configuration Guide
###################

After installation, you will need to create a configuration file in a directory dedicated to ``pattoo``.


*********************
Configuration Options
*********************

There are two ways to configure ``pattoo``. These are the:

#. Quick Method
#. Expert Method

Quick Method
============

Use the quick method if you are new to ``pattoo``.

Run the ``setup/install.py`` script.  The configuration values will be automatically set.

Here's the command to run:

.. code-block:: bash

  $ sudo setup/install.py install configuration

Expert Method
=============

This section goes into configuration parameters in great detail.

Setting the  Configuration Directory Location
---------------------------------------------

By default, the configuration directory for all pattoo components is set to ``/etc/pattoo``, which is owned by the pattoo user


Copy the Template to Your Configuration Directory
-------------------------------------------------

You can create your first ``pattoo.yaml`` configuration file by copying the template file in the ``examples/etc`` directory to the ``/etc/pattoo`` location.

**NOTE:** If a ``/path/to/configuration/directory/pattoo.yaml`` file already exists in the directory then skip this step and edit the file according to the steps in following sections.

.. code-block:: bash

    $ cp examples/etc/pattoo.yaml.template \
      /path/to/configuration/directory/pattoo.yaml

The next step is to edit the contents of ``pattoo.yaml``

Edit Your Configuration
-----------------------

Take some time to read up on ``YAML`` formatted files if you are not familiar with them. A background knowledge is always helpful.

The ``pattoo.yaml`` file created from the template will have sections that you will need to edit with custom values. Don't worry, these sections are easily identifiable as they all start with ``PATTOO_``

**NOTE:** The indentations in the YAML configuration are important. Make sure indentations line up. Dashes '-' indicate one item in a list of items (if applicable).

.. code-block:: yaml

   pattoo:

       log_level: debug
       log_directory: PATTOO_LOG_DIRECTORY
       cache_directory: PATTOO_CACHE_DIRECTORY
       daemon_directory: PATTOO_DAEMON_DIRECTORY
       system_daemon_directory: PATTOO_SYSTEM_DAEMON_DIRECTORY
       language: en

   pattoo_agent_api:

       ip_address: 192.168.1.100
       ip_bind_port: 20201

Configuration Explanation
^^^^^^^^^^^^^^^^^^^^^^^^^

This table outlines the purpose of each configuration parameter

.. list-table::
   :header-rows: 1

   * - Section
     - Config Options
     - Description
   * - ``pattoo``
     -
     - This section defines the locations of key directories for both operation and troubleshooting
   * -
     - ``log_directory``
     - Path to logging directory. Make sure the username running the daemons have RW access to files there.
   * -
     - ``log_level``
     - Default level of logging. ``debug`` is best for troubleshooting.
   * -
     - ``cache_directory``
     - Directory of unsuccessful data posts to ``pattoo``
   * -
     - ``daemon_directory``
     - Directory used to store daemon related data that needs to be maintained between reboots
   * -
     - ``system_daemon_directory``
     - Directory used to store daemon related data that should be deleted between reboots. This should only be configured if you are running ``pattoo`` daemons as ``systemd`` daemons. The ``systemd`` daemon installation procedure automatically adjusts this configuration. This parameter defaults to the ``daemon_directory`` value if it is not configured. 
   * -
     - ``language``
     - Language spoken by the human users of ``pattoo``. Defaults to ``en`` (English)
   * - ``pattoo_agent_api``
     -
     - This section provides information needed by ``pattoo`` agent clients when contacting the pattoo server
   * -
     - ``ip_address``
     - IP address of remote ``pattoo`` server
   * -
     - ``ip_bind_port``
     - Port of remote ``pattoo`` server accepting agent data. Default 20201.


Agent Configuration
-------------------

You will now need to configure each agent individually. See the :doc:`agent` file for details on how to configure each type of agent.