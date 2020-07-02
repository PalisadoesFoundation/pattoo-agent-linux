#!/usr/bin/env python3
"""This is a test of flask."""

# Pip packages
from flask import Flask, jsonify

# Pattoo imports
from pattoo_agent_os import collector
from pattoo_shared import converter
from pattoo_agent_os import (
    PATTOO_AGENT_OS_SPOKED_API_PREFIX, PATTOO_AGENT_OS_SPOKED)


# Define flask parameters
API = Flask(__name__)


@API.route(
    '{}/<int:polling_interval>'.format(PATTOO_AGENT_OS_SPOKED_API_PREFIX))
def home(polling_interval):
    """Display api data on home page.

    Args:
        polling_interval: Polling interval of the requester

    Returns:
        None

    """
    # Process and present
    agentdata = collector.poll(PATTOO_AGENT_OS_SPOKED, polling_interval)
    pdp = converter.agentdata_to_post(agentdata)
    result = converter.posting_data_points(pdp)
    return jsonify(result)
