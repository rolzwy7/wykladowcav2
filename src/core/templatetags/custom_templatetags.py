from django import template

register = template.Library()


def startswith(startswith_base: str, startswith_value: str) -> bool:
    """Checks if given string starts with given value

    Args:
        starletswith_base (str): string
        startswith_value (str): value

    Returns:
        bool: True if string starts with value, False otherwise
    """
    return startswith_base.startswith(startswith_value)


register.filter("startswith", startswith)


def shorten(base: str, length: int) -> str:
    """Shorten string by cutting it and ending at the end `...`

    Args:
        base (str): base string
        length (int): length

    Returns:
        str: shortened string
    """

    if len(base) <= length:
        return base

    return f"{base[:length]}" + "..."


register.filter("shorten", shorten)
