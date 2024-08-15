"""
Lecturer opinion admin
"""

from django.contrib.admin import ModelAdmin, register

from core.models import LecturerOpinion


@register(LecturerOpinion)
class LecturerOpinionModelAdmin(ModelAdmin):
    """LecturerOpinionModelAdmin"""

    search_fields = [
        "fullname",
        "job_title",
        "opinion_text",
        "lecturer_reply",
        "company_name",
    ]
    list_display = [
        "fullname",
        "rating",
        "lecturer",
        "job_title",
        "company_name",
        "flagship_opinion",
    ]

    list_filter = [
        "flagship_opinion",
        "visible_on_page",
        "added_on_website",
        "lecturer",
        "rating",
    ]

    date_hierarchy = "created_at"
