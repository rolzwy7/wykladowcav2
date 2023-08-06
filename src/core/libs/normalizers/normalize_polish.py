def normalize_polish(text: str) -> str:
    """Convert text to lowercase. Replace polish letters with roman alphabet.

    Examples:
    Kość -> kosc
    WąS -> was

    Args:
        text (str): text to be normalized

    Returns:
        str: normalized text
    """
    letters_map = {
        "ą": "a",
        "ć": "c",
        "ę": "e",
        "ł": "l",
        "ń": "n",
        "ś": "s",
        "ó": "o",
        "ż": "z",
        "ź": "z",
    }
    temp = text.lower()
    for letter, replacement in letters_map.items():
        temp = temp.replace(letter, replacement)
    return temp
