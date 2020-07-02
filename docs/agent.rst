
Agent Documentation
===================

``pattoo`` comes with a number of standard agents, but you can also create your own custom agents to meet your needs. Both approaches are described here.

``pattoo`` Standard Agents
--------------------------

Here is a description of currently supported ``pattoo`` agents.

.. list-table::
   :header-rows: 1

   * - Agent
     - Description
     - Documenatation
   * - ``pattoo_agent_modbustcpd``
     - Python3 based daemon that polls remote ``ip_devices`` for Modbus data over TCP.
     - Documentation can be found here. :doc:`pattoo_agent_modbustcpd`
   * - ``pattoo_agent_os_spoked``
     - Python3 based daemon that presents ``pattoo`` data via a web API URL. This data can be regularly polled from a central server
     - Documentation can be found here. :doc:`pattoo_agent_os`
   * - ``pattoo_agent_os_hubd``
     - Python3 based daemon that polls ``pattoo_agent_os_spoked`` APIs for data.
     - Documentation can be found here. :doc:`pattoo_agent_os`
   * - ``pattoo_agent_os_autonomousd``
     - Python3 based daemon that posts  ``pattoo`` to a central server.
     - Documentation can be found here. :doc:`pattoo_agent_os_autonomousd`
   * - ``pattoo_agent_snmpd``
     - Python3 based daemon that polls remote ``ip_devices`` for SNMP data.
     - Documentation can be found here. :doc:`pattoo_agent_snmpd`
   * - ``pattoo_agent_snmp_ifmibd``
     - Python3 based daemon that polls remote ``ip_devices`` for SNMP ifMIB data.
     - Documentation can be found here. :doc:`pattoo_agent_snmp_ifmibd`

Creating Custom Agents
----------------------

Please visit the `Pattoo Shared documentation site <https://pattoo-shared.readthedocs.io/en/latest/agents.html>`_ to see how it is done.
