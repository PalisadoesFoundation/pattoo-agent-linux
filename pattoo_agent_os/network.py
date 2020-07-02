"""Module used to manage network resources."""

# Import PIP libraries
import ipaddress
import socket


def get_ip_address(device):
    """Get IP address for a device.

    Args:
        device: Device for which address is required

    Returns:
        result: IP address

    """
    # Initialize key variables
    result = None

    # Check if IP address
    try:
        _ = ipaddress.ip_address(device)
        result = device
    except:
        # Not an IP address
        try:
            result = socket.gethostbyname(device)
        except:
            result = None

    # Return
    return result
