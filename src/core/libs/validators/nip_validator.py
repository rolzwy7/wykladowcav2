from django.core.exceptions import ValidationError


def validate_nip(nip: str) -> bool:
    """Validates NIP number (no spaces of dashes)

    Args:
        nip (str): NIP number

    Returns:
        bool: True if valid, False otherwise
    """
    # Remove any whitespace or dashes
    nip = nip.replace(" ", "").replace("-", "")

    # Check if the length is correct
    if len(nip) != 10:
        return False

    # Check if the NIP consists of digits only
    if not nip.isdigit():
        return False

    # Calculate the checksum
    weights = [6, 5, 7, 2, 3, 4, 5, 6, 7]
    checksum = sum(int(nip[i]) * weights[i] for i in range(9)) % 11

    # Check if the checksum is correct
    if checksum != int(nip[9]):
        return False

    return True


def validate_nip_modelfield(nip: str):
    """NIP validator for model field"""
    if not validate_nip(nip):
        raise ValidationError(
            "Wprowadzony NIP `%(nip)s` nie jest poprawny",
            params={"nip": nip},
        )
