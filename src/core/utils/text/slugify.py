from django.utils.text import slugify as django_slugify


def slugify(value: str):
    """Modified `django.utils.text.slugify` function for polish letters"""
    letters_map = {
        "ą": "a",
        "ć": "c",
        "ę": "e",
        "ł": "l",
        "ń": "n",
        "ó": "o",
        "ś": "s",
        "ż": "z",
        "ź": "z",
    }
    modified_value = value.lower()
    for letter_from, letter_to in letters_map.items():
        modified_value = modified_value.replace(letter_from, letter_to)
    return django_slugify(modified_value, allow_unicode=True)
