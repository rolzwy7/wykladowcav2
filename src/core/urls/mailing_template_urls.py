# flake8: noqa:E501
# pylint: disable=line-too-long

from django.urls import path

from core.views.mailing_templates import (
    global_mailing_editor_page,
    global_mailing_template_page,
    lecturer_mailing_template_page,
    webinar_category_mailing_editor_page,
    webinar_category_mailing_template_page,
)

urlpatterns = [
    # Global mailing template
    path(
        "globalny-szablon-mailingowy/",
        global_mailing_template_page,
        name="global_mailing_template",
    ),
    path(
        "globalny-edytor-mailingowy/",
        global_mailing_editor_page,
        name="global_mailing_editor",
    ),
    # Lecturer
    # path(
    #     "zbiorcze-wykladowca/<slug:slug>/mailing-zestawienie/",
    #     lecturer_mailing_template_page,
    #     name="lecturer_mailing_template_page",
    # ),
    # # Category
    # path(
    #     "zbiorcze-kategoria/<slug:slug>/edytor-mailingowy/",
    #     webinar_category_mailing_editor_page,
    #     name="webinar_category_mailing_editor_page",
    # ),
    # path(
    #     "zbiorcze-kategoria/<slug:slug>/szablon-mailingowy/",
    #     webinar_category_mailing_template_page,
    #     name="webinar_category_mailing_template_page",
    # ),
    # Webinar
    # path(
    #     "oferta-webinar/<int:pk>/edytor-mailingowy/",
    #     webinar_mailing_editor_page,
    #     name="webinar_mailing_editor_page",
    # ),
    # path(
    #     "oferta-webinar/<int:pk>/szablon-mailingowy/",
    #     webinar_mailing_template_page,
    #     name="webinar_mailing_template_page",
    # ),
]
