Basic Installation
==================

This section covers some key steps to get you started.

Prerequisites
-------------

There are some software components that need to be installed prior to starting.

#. ``pattoo`` only runs on Python 3.6 or higher

Let's install the software.

Installation
------------

Follow these steps.

#. Install ``git`` on your system.
#. Select and create the parent directory in which you want to install ``pattoo-agent-linux``.

    .. code-block:: bash

       $ mkdir -p /installation/parent/directory
       $ cd /installation/parent/directory

#. Clone the repository to the parent directory using the ``git clone`` command. You can also choose to downloading and unzip the file in the parent directory. The repository can be found at: https://github.com/PalisadoesFoundation/pattoo-agent-linux.

**Note** The repository should not be cloned to a directory with ``/home`` in its path

    .. code-block:: bash

       $ cd /installation/parent/directory
       $ git clone https://github.com/PalisadoesFoundation/pattoo-agent-linux.git

4. Enter the ``/installation/parent/directory/pattoo-agent-linux`` directory with the ``pattoo-agent-linux`` files. 

   .. code-block:: bash

      $ pip3 install --user PattooShared
      $ pip3 install --user virtualenv

#. Use the :doc:`configuration` to create a working configuration.
#. Follow the configuration steps for each daemon as explained in the :doc:`agent`.

Running the installation
---------------------------
Run the code block below to install the BACnet agent

   .. code-block:: bash

      $ sudo setup/install.py install all


Stopping, Starting and Restarting daemons
------------------------------------------
By default, the installation starts the daemons, and restarts them if they are already running, however, if you desire to start, stop or restart the system daemon for the linux agent after the installation the following code blocks should assist:

**Starting daemon**
   .. code-block:: bash

      $ sudo systemctl start <daemon_name>.service 

**Stopping daemon**
   .. code-block:: bash

      $ sudo systemctl stop <daemon_name>.service 

**Restarting daemon**
   .. code-block:: bash

      $ sudo systemctl restart <daemon_name>.service 

Modifying configuration files
---------------------------------

Navigate to the  ``/etc/pattoo``  directory to modify the configuration files for the linux agent using your desired text editor, with the code block below:
The three configuration files for the linux agent are:

   .. code-block:: bash

      $ cd /etc/pattoo