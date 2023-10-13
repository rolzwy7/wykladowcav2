from typing import Union

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AnonymousUser

from core.exceptions import UnauthorizedException


def deny_if_not_staff(user: Union[AbstractBaseUser, AnonymousUser]):
    """Raise `401 Unauthorized` if user is not authenticated staff member

    Args:
        user (Union[AbstractBaseUser, AnonymousUser]): user

    Raises:
        UnauthorizedException: raises 401
    """
    if any(
        [
            not user.is_authenticated,
            not user.is_staff,  # type: ignore
        ]
    ):
        raise UnauthorizedException()
