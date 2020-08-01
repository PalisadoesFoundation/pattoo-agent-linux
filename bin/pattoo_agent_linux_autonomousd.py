#!/usr/bin/env python3
"""Pattoo multi-user operating system reporter daemon.

Posts system data to remote host over HTTP.

"""

# Standard libraries
from __future__ import print_function
from time import sleep, time
import sys
import os

# Try to create a working PYTHONPATH
_BIN_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
_ROOT_DIRECTORY = os.path.abspath(os.path.join(_BIN_DIRECTORY, os.pardir))
_EXPECTED = '{0}pattoo-agent-linux{0}bin'.format(os.sep)
if _BIN_DIRECTORY.endswith(_EXPECTED) is True:
    sys.path.append(_ROOT_DIRECTORY)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

# Pattoo libraries
from pattoo_shared import log
from pattoo_shared.agent import Agent, AgentCLI
from pattoo_shared.phttp import PostAgent
from pattoo_agent_linux import PATTOO_AGENT_LINUX_AUTONOMOUSD
from pattoo_agent_linux import collector
from pattoo_agent_linux.configuration import ConfigAutonomousd as Config


class PollingAgent(Agent):
    """Agent that gathers data."""

    def __init__(self, parent):
        """Initialize the class.

        Args:
            config_dir: Configuration directory

        Returns:
            None

        """
        # Initialize key variables
        Agent.__init__(self, parent)
        self._parent = parent

    def query(self):
        """Query all remote targets for data.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        config = Config()
        _pi = config.polling_interval()

        # Post data to the remote server
        while True:
            # Get start time
            ts_start = time()

            # Get system data
            agentdata = collector.poll(self._parent, _pi)

            # Post to remote server
            server = PostAgent(agentdata)

            # Post data
            success = server.post()

            # Purge cache if success is True
            if success is True:
                server.purge()

            # Sleep
            duration = time() - ts_start
            sleep(abs(_pi - duration))


def main():
    """Start the pattoo agent.

    Args:
        None

    Returns:
        None

    """
    # Get configuration
    agent_poller = PollingAgent(PATTOO_AGENT_LINUX_AUTONOMOUSD)

    # Do control
    cli = AgentCLI()
    cli.control(agent_poller)


if __name__ == "__main__":
    log.env()
    main()
