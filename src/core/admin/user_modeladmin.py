"""
User model admin
"""

from django.contrib.admin import ModelAdmin, register

from core.models import User


@register(User)
class UserModelAdmin(ModelAdmin):
    """UserModelAdmin"""

    ...
