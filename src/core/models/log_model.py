"""SystemLog Model"""

# flake8: noqa:E501
# pylint: disable=line-too-long
import uuid

from django.conf import settings
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    EmailField,
    ImageField,
    Index,
    Manager,
    ManyToManyField,
    Model,
    OneToOneField,
    PositiveIntegerField,
    Q,
    QuerySet,
    SlugField,
    TextField,
    UUIDField,
)
from django.urls import reverse

from core.consts import SLUG_HELP_TEXT
from core.utils.text import slugify

BASE_URL = settings.BASE_URL


class SystemLogModelManager(Manager):
    """SystemLogModelManager"""

    # def get_lecturers_visible_on_page(self) -> QuerySet["Lecturer"]:
    #     """Returns lecturers that are visible on website"""
    #     return self.get_queryset().filter(visible_on_page=True)


class SystemLogModel(Model):
    LOG_TYPE_CHOICES = (
        ("INFO", "Info"),
        ("DEBUG", "Debug"),
        ("ERROR", "Error"),
        ("WARNING", "Warning"),
        ("CRITICAL", "Critical"),
    )

    manager = SystemLogModelManager()

    timestamp = DateTimeField(auto_now_add=True)
    log_type = CharField(max_length=20, choices=LOG_TYPE_CHOICES, default="INFO")
    message = TextField()
    source = CharField(
        max_length=100, null=True, blank=True
    )  # e.g., module or service name
    stack_trace = TextField(null=True, blank=True)  # For error details

    class Meta:
        """Meta"""

        ordering = ["-timestamp"]
        verbose_name = "System Log"
        verbose_name_plural = "System Logs"
        indexes = [
            Index(fields=["source"]),
        ]

    def __str__(self):
        return f"{self.timestamp} - {self.log_type} - {self.source or 'System'}"
