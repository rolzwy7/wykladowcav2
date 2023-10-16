import re


def normalize_phone_number(phone_number: str) -> str:
    """Normalize phone number if it matches one of the regular expression

    If phone number doesn't match regular expression return it
    without normalizing.

    Args:
        phone_number (str): phone number

    Returns:
        str: normalized phone number
    """

    match = re.match(r"(\+48|)(| )([0-9]{9})", phone_number)
    if match:
        ph_group = match.group(3)
        ret = f"{ph_group[:3]} {ph_group[3:6]} {ph_group[6:9]}"
    else:
        ret = phone_number

    return ret
