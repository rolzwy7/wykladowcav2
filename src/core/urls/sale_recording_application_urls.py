from django.urls import path

from core.views.sale_recording_application import (
    sale_recording_application_buyer_page,
    sale_recording_application_buyer_recipient_page,
    sale_recording_application_invoice_page,
    sale_recording_application_participants_page,
    sale_recording_application_person_details_page,
    sale_recording_application_success_page,
    sale_recording_application_summary_page,
    sale_recording_application_type_page,
)

urlpatterns = [
    path(
        "<int:pk>/typ-zgloszenia/",
        sale_recording_application_type_page,
        name="sale_recording_application_type_page",
    ),
    path(
        "<uuid:uuid>/nabywca/",
        sale_recording_application_buyer_page,
        name="sale_recording_application_buyer_page",
    ),
    path(
        "<uuid:uuid>/nabywca-odbiorca/",
        sale_recording_application_buyer_recipient_page,
        name="sale_recording_application_buyer_recipient_page",
    ),
    path(
        "<uuid:uuid>/faktura/",
        sale_recording_application_invoice_page,
        name="sale_recording_application_invoice_page",
    ),
    # path(
    #     "<uuid:uuid>/osoba-zglaszajaca/",
    #     application_submitter_page,
    #     name="application_submitter_page",
    # ),
    path(
        "<uuid:uuid>/osoba-prywatna/",
        sale_recording_application_person_details_page,
        name="sale_recording_application_person_details_page",
    ),
    path(
        "<uuid:uuid>/uczestnicy/",
        sale_recording_application_participants_page,
        name="sale_recording_application_participants_page",
    ),
    # path(
    #     "<uuid:uuid>/dodatkowe-uwagi/",
    #     application_additional_information_page,
    #     name="application_additional_information_page",
    # ),
    path(
        "<uuid:uuid>/podsumowanie/",
        sale_recording_application_summary_page,
        name="sale_recording_application_summary_page",
    ),
    # path(
    #     "<uuid:uuid>/karta-zgloszeniowa/",
    #     application_pdf_card,
    #     name="application_pdf_card",
    # ),
    # path(
    #     "wybierz-termin/<str:grouping_token>/",
    #     application_choose_webinar,
    #     name="application_choose_webinar",
    # ),
    path(
        "wyslano/",
        sale_recording_application_success_page,
        name="sale_recording_application_success_page",
    ),
]
