from django.urls import path

from core.views.lecturer import (
    lecturer_closed_webinar_pages,
    lecturer_experience_page,
    lecturer_mailing_template_page,
    lecturer_opinion_form_page,
    lecturer_opinion_thanks,
    lecturer_opinions_page,
    lecturer_webinars_page,
)

urlpatterns = [
    path(
        "<slug:slug>/",
        lecturer_experience_page,
        name="lecturer_experience_page",
    ),
    path(
        "<slug:slug>/opinie/",
        lecturer_opinions_page,
        name="lecturer_opinions_page",
    ),
    path(
        "<slug:slug>/szkolenia/",
        lecturer_webinars_page,
        name="lecturer_webinars_page",
    ),
    path(
        "<slug:slug>/szkolenia-zamkniete/",
        lecturer_closed_webinar_pages,
        name="lecturer_closed_webinar_pages",
    ),
    path(
        "<slug:slug>/mailing-zestawienie/",
        lecturer_mailing_template_page,
        name="lecturer_mailing_template_page",
    ),
    path(
        "<slug:slug>/przeslij-opinie/",
        lecturer_opinion_form_page,
        name="lecturer_opinion_form_page",
    ),
    path(
        "<slug:slug>/dziekujemy-za-przeslanie-opinii/",
        lecturer_opinion_thanks,
        name="lecturer_opinion_thanks",
    ),
]
