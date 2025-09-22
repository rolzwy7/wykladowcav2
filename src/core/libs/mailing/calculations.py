"""
Mailing calculations
"""

# flake8: noqa=E501

import math


def total_sending_time(
    total_emails: int,
    batch_size: int,
    sleep_per_email: float,
    sleep_between_batches: int,
):
    """
    Calculate total mailing time based on number of emails, batch size, and sleep intervals.

    Args:
        total_emails (int): Total number of emails to send
        batch_size (int): Number of emails per batch
        sleep_per_email (int): Seconds to sleep after each email
        sleep_between_batches (int): Seconds to sleep between batches

    Returns:
        int: Total time in seconds
    """
    # Calculate number of batches (ceiling division)
    num_batches = math.ceil(total_emails / batch_size)

    # Time for sending emails: total_emails * sleep_per_email
    send_time = total_emails * sleep_per_email

    # Time for sleeps between batches: (num_batches - 1) * sleep_between_batches
    batch_sleep_time = (num_batches - 1) * sleep_between_batches

    # Total time
    total_time = send_time + batch_sleep_time

    return total_time
