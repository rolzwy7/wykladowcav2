# """Log Model"""

# # flake8: noqa:E501
# # pylint: disable=line-too-long
# import uuid

# from django.conf import settings
# from django.db.models import (
#     CASCADE,
#     BooleanField,
#     CharField,
#     DateTimeField,
#     EmailField,
#     ImageField,
#     Manager,
#     ManyToManyField,
#     Model,
#     OneToOneField,
#     PositiveIntegerField,
#     Q,
#     QuerySet,
#     SlugField,
#     TextField,
#     UUIDField,
# )
# from django.urls import reverse

# from core.consts import SLUG_HELP_TEXT
# from core.utils.text import slugify

# BASE_URL = settings.BASE_URL


# class LogiModelManager(Manager):
#     """Lecturer query Manager"""

#     def get_lecturers_visible_on_page(self) -> QuerySet["Lecturer"]:
#         """Returns lecturers that are visible on website"""
#         return self.get_queryset().filter(visible_on_page=True)


# class LogiModel(Model):
#     """This model represents Lecturer"""

#     manager = LecturerManager()

#     uuid = UUIDField("Identyfikator certyfikatu", default=uuid.uuid4, unique=True)

#     created_at = DateTimeField(auto_now_add=True)
#     updated_at = DateTimeField(auto_now=True)

#     category = CharField(
#         "Kategoria",
#         max_length=64,
#         db_index=True,
#         default="default",
#         help_text="Kategoria logu",
#     )

#     subcategory = CharField(
#         "Subkategoria",
#         max_length=64,
#         db_index=True,
#         default="default",
#         help_text="Subkategoria logu",
#     )

#     description = TextField(
#         "Logi",
#         blank=True,
#         help_text="Logi",
#     )

#     class Meta:
#         verbose_name = "Logi"
#         verbose_name_plural = "Logi"

#     def save(self, *args, **kwargs) -> None:
#         return super().save(*args, **kwargs)
