#!/usr/bin/env python3
"""Pattoo multi-user operating system reporter daemon.

Serves system data to remote clients over HTTP.

Uses a Gunicorn WSGI entry point to serve data.

"""


# Standard libraries
from __future__ import print_function
import sys
import os

# Try to create a working PYTHONPATH
_BIN_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
_ROOT_DIRECTORY = os.path.abspath(os.path.join(_BIN_DIRECTORY, os.pardir))
_EXPECTED = '{0}pattoo-agent-os{0}bin'.format(os.sep)
if _BIN_DIRECTORY.endswith(_EXPECTED) is True:
    sys.path.append(_ROOT_DIRECTORY)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

# Pattoo libraries
from pattoo_shared import log
from pattoo_shared.agent import Agent, AgentAPI, AgentCLI
from pattoo_agent_os import (
    PATTOO_AGENT_OS_SPOKED, PATTOO_AGENT_OS_SPOKED_PROXY)
from pattoo_agent_os import configuration
from pattoo_agent_os.api import API


def main():
    """Control the Gunicorn WSGI."""
    # Create Gunicorn object to daemonize
    agent_api = Agent(PATTOO_AGENT_OS_SPOKED_PROXY)

    # Create Flask object to daemonize
    config = configuration.ConfigSpoked()
    agent_gunicorn = AgentAPI(
        PATTOO_AGENT_OS_SPOKED,
        PATTOO_AGENT_OS_SPOKED_PROXY,
        API,
        config=config)

    # Do control (Gunicorn first, Daemonized query second)
    cli = AgentCLI()
    cli.control(agent_gunicorn)
    cli.control(agent_api)


if __name__ == '__main__':
    log.env()
    main()
