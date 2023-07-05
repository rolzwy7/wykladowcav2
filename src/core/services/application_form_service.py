from typing import Optional
from uuid import UUID

from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse

from core.consts import VAT_EXEMPTION_0
from core.exceptions import RedirectException
from core.models import (
    Webinar,
    WebinarApplication,
    WebinarApplicationInvoice,
    WebinarApplicationPrivatePerson,
    WebinarApplicationSubmitter,
    WebinarParticipant,
)
from core.models.enums import WebinarApplicationStep, WebinarApplicationType

APPLICATION_TYPE = WebinarApplicationStep.APPLICATION_TYPE
BUYER = WebinarApplicationStep.BUYER
RECIPIENT = WebinarApplicationStep.RECIPIENT
INVOICE = WebinarApplicationStep.INVOICE
SUBMITTER = WebinarApplicationStep.SUBMITTER
PARTICIPANTS = WebinarApplicationStep.PARTICIPANTS
ADDITIONAL_INFO = WebinarApplicationStep.ADDITIONAL_INFO
SUMMARY = WebinarApplicationStep.SUMMARY
PERSON_DETAILS = WebinarApplicationStep.PERSON_DETAILS

COMPANY = WebinarApplicationType.COMPANY
JSFP = WebinarApplicationType.JSFP
PRIVATE_PERSON = WebinarApplicationType.PRIVATE_PERSON


class ApplicationFormService:
    """Represents application step state"""

    def __init__(
        self,
        webinar: Webinar,
        application: WebinarApplication,
        current_step: str,
    ) -> None:
        self.webinar = webinar
        self.application = application
        self.application_type = application.application_type
        self.current_step = current_step

    @staticmethod
    def get_application_type_redirect(application_type: str, uuid: UUID):
        """First redirect after application type selection step"""
        url_names = {
            COMPANY: "application_buyer_page",
            JSFP: "application_buyer_page",
            PRIVATE_PERSON: "application_person_details_page",
        }
        url_name = url_names[application_type]
        return redirect(reverse(f"core:{url_name}", kwargs={"uuid": uuid}))

    def get_timeline(self):
        """Returns step's timeline"""
        buyer_nip = self.application.buyer.nip if self.application.buyer else ""
        recipient_nip = (
            self.application.recipient.nip if self.application.recipient else ""
        )

        invoice: Optional[WebinarApplicationInvoice] = self.application.invoice
        if invoice:
            invoice_type = invoice.get_invoice_type_display()  # type: ignore
            invoice_email = invoice.invoice_email
            if invoice.vat_exemption != VAT_EXEMPTION_0.db_key:
                is_vat_exempt = "Zwolnienie z VAT"
            else:
                is_vat_exempt = ""
        else:
            invoice_type = ""
            invoice_email = ""
            is_vat_exempt = ""

        submitter_fullname = (
            self.application.submitter.fullname
            if self.application.submitter
            else ""
        )
        participants_count = WebinarParticipant.manager.filter(
            application=self.application
        ).count()
        participants_conj = (
            f"{participants_count} uczestnik"
            if participants_count == 1
            else f"{participants_count} uczestników"
        )

        is_additional_info = (
            "Uwagi zapisane"
            if self.application.additional_information
            else "Brak uwag"
        )

        company_map = {
            APPLICATION_TYPE: [],
            BUYER: [("Nabywca", "-", True, "")],
            INVOICE: [
                ("Nabywca", f"NIP {buyer_nip}", False, ""),
                ("Faktura", "-", True, ""),
            ],
            SUBMITTER: [
                ("Nabywca", f"NIP {buyer_nip}", False, ""),
                (invoice_type, invoice_email, False, is_vat_exempt),
                ("Osoba zgłaszająca", "-", True, ""),
            ],
            PARTICIPANTS: [
                ("Nabywca", f"NIP {buyer_nip}", False, ""),
                (invoice_type, invoice_email, False, is_vat_exempt),
                ("Osoba zgłaszająca", submitter_fullname, False, ""),
                ("Uczestnicy", "-", True, ""),
            ],
            ADDITIONAL_INFO: [
                ("Nabywca", f"NIP {buyer_nip}", False, ""),
                (invoice_type, invoice_email, False, is_vat_exempt),
                ("Osoba zgłaszająca", submitter_fullname, False, ""),
                ("Uczestnicy", participants_conj, False, ""),
                ("Dodatkowe uwagi", "-", True, ""),
            ],
            SUMMARY: [
                ("Nabywca", f"NIP {buyer_nip}", False, ""),
                (invoice_type, invoice_email, False, is_vat_exempt),
                ("Osoba zgłaszająca", submitter_fullname, False, ""),
                ("Uczestnicy", participants_conj, False, ""),
                ("Dodatkowe uwagi", is_additional_info, False, ""),
                ("Podsumowanie", "", True, ""),
            ],
        }

        jsfp_map = {
            APPLICATION_TYPE: [],
            BUYER: [("Nabywca", "-", True, "")],
            RECIPIENT: [
                ("Nabywca", f"NIP {buyer_nip}", False, ""),
                ("Odbiorca", "-", True, ""),
            ],
            INVOICE: [
                ("Nabywca", f"NIP {buyer_nip}", False, ""),
                ("Odbiorca", f"NIP {recipient_nip}", False, ""),
                ("Faktura", "-", True, ""),
            ],
            SUBMITTER: [
                ("Nabywca", f"NIP {buyer_nip}", False, ""),
                ("Odbiorca", f"NIP {recipient_nip}", False, ""),
                (invoice_type, invoice_email, False, is_vat_exempt),
                ("Osoba zgłaszająca", "-", True, ""),
            ],
            PARTICIPANTS: [
                ("Nabywca", f"NIP {buyer_nip}", False, ""),
                ("Odbiorca", f"NIP {recipient_nip}", False, ""),
                (invoice_type, invoice_email, False, is_vat_exempt),
                ("Osoba zgłaszająca", submitter_fullname, False, ""),
                ("Uczestnicy", "-", True, ""),
            ],
            ADDITIONAL_INFO: [
                ("Nabywca", f"NIP {buyer_nip}", False, ""),
                ("Odbiorca", f"NIP {recipient_nip}", False, ""),
                (invoice_type, invoice_email, False, is_vat_exempt),
                ("Osoba zgłaszająca", submitter_fullname, False, ""),
                ("Uczestnicy", participants_conj, False, ""),
                ("Dodatkowe uwagi", "-", True, ""),
            ],
            SUMMARY: [
                ("Nabywca", f"NIP {buyer_nip}", False, ""),
                ("Odbiorca", f"NIP {recipient_nip}", False, ""),
                (invoice_type, invoice_email, False, is_vat_exempt),
                ("Osoba zgłaszająca", submitter_fullname, False, ""),
                ("Uczestnicy", participants_conj, False, ""),
                ("Dodatkowe uwagi", is_additional_info, False, ""),
                ("Podsumowanie", "", True, ""),
            ],
        }

        private_person_map = {
            PERSON_DETAILS: [("Twoje dane", "", True, "")],
            ADDITIONAL_INFO: [
                ("Twoje dane", "", False, ""),
                ("Dodatkowe uwagi", "-", True, ""),
            ],
            SUMMARY: [
                ("Twoje dane", "", False, ""),
                ("Dodatkowe uwagi", is_additional_info, False, ""),
                ("Podsumowanie", "", True, ""),
            ],
        }

        steps_map = {
            COMPANY: company_map,
            JSFP: jsfp_map,
            PRIVATE_PERSON: private_person_map,
        }

        return steps_map[self.application_type][self.current_step]

    def get_step_number(self):
        """Returns step number"""
        next_step_map = {
            COMPANY: {
                BUYER: "1",
                INVOICE: "2",
                SUBMITTER: "3",
                PARTICIPANTS: "4",
                ADDITIONAL_INFO: "5",
                SUMMARY: "6",
            },
            JSFP: {
                BUYER: "1",
                RECIPIENT: "2",
                INVOICE: "3",
                SUBMITTER: "4",
                PARTICIPANTS: "5",
                ADDITIONAL_INFO: "6",
                SUMMARY: "7",
            },
            PRIVATE_PERSON: {
                PERSON_DETAILS: "1",
                ADDITIONAL_INFO: "2",
                SUMMARY: "3",
            },
        }
        return next_step_map[self.application_type].get(self.current_step, "?")

    def get_step_title(self):
        """Returns application's step title"""
        title_map = {
            APPLICATION_TYPE: "Wybierz typ zgłoszenia",
            BUYER: "Nabywca",
            RECIPIENT: "Odbiorca",
            PERSON_DETAILS: "Osoba prywatna",
            INVOICE: "Faktura",
            SUBMITTER: "Osoba Zgłaszająca",
            PARTICIPANTS: "Uczestnicy",
            ADDITIONAL_INFO: "Dodatkowe informacje (opcjonalnie)",
            SUMMARY: "Podsumowanie zgłoszenia",
        }
        return title_map.get(self.current_step, "{DEFAULT TITLE}")

    def get_step_description(self):
        """Returns step description"""
        description_map = {
            APPLICATION_TYPE: "",
            BUYER: "Wprowadź dane nabywcy",
            RECIPIENT: "Wprowadź dane odbiorcy",
            PERSON_DETAILS: "Wprowadź swoje dane",
            INVOICE: (
                "Wypełnij dane dotyczące Faktury"
                " i Zwolenienia z VAT (jeśli dotyczy)"
            ),
            SUBMITTER: "Wprowadź dane osoby wysyłającej zgłoszenie",
            PARTICIPANTS: "Wprowadź dane uczestników webinaru",
            ADDITIONAL_INFO: (
                "Jeśli mają Państwo dodatkowe uwagi związane ze zgłoszeniem"
                " prosimy wpisać je tutaj"
            ),
            SUMMARY: (
                "Prosimy o sprawdzenie poprawności podanych danych."
                " W razie zauważenia pomyłek należy użyć przycisku"
                " „Popraw zgłoszenie”"
            ),
        }
        return description_map.get(self.current_step, "{DEFAULT DESCRIPTION}")

    def get_previous_step_url(self):
        """Returns application previous step URL"""
        previous_step_map = {
            COMPANY: {
                BUYER: (None, ""),
                INVOICE: ("application_buyer_page", "Wróć do Nabywcy"),
                SUBMITTER: ("application_invoice_page", "Wróć do Faktury"),
                PARTICIPANTS: (
                    "application_submitter_page",
                    "Wróć do Osoby Zgłaszającej",
                ),
                ADDITIONAL_INFO: (
                    "application_participants_page",
                    "Wróć do Uczestników",
                ),
                SUMMARY: (None, ""),
            },
            JSFP: {
                BUYER: (None, ""),
                RECIPIENT: ("application_buyer_page", "Wróć do Nabywcy"),
                INVOICE: ("application_recipient_page", "Wróć do Odbiorcy"),
                SUBMITTER: ("application_invoice_page", "Wróć do Faktury"),
                PARTICIPANTS: (
                    "application_submitter_page",
                    "Wróć do Osoby Zgłaszającej",
                ),
                ADDITIONAL_INFO: (
                    "application_participants_page",
                    "Wróć do Uczestników",
                ),
                SUMMARY: (None, ""),
            },
            PRIVATE_PERSON: {
                PERSON_DETAILS: (None, ""),
                ADDITIONAL_INFO: ("application_person_details_page", "Wróć"),
                SUMMARY: (None, ""),
            },
        }
        url_name, title = previous_step_map[self.application_type][
            self.current_step
        ]
        if url_name is None:
            return ("", title)
        else:
            return (
                reverse(
                    f"core:{url_name}", kwargs={"uuid": self.application.uuid}
                ),
                title,
            )

    def get_next_step_url(self):
        """Returns application's next step url"""
        url_names = {
            COMPANY: {
                BUYER: "application_invoice_page",
                INVOICE: "application_submitter_page",
                SUBMITTER: "application_participants_page",
                PARTICIPANTS: "application_additional_information_page",
                ADDITIONAL_INFO: "application_summary_page",
            },
            JSFP: {
                BUYER: "application_recipient_page",
                RECIPIENT: "application_invoice_page",
                INVOICE: "application_submitter_page",
                SUBMITTER: "application_participants_page",
                PARTICIPANTS: "application_additional_information_page",
                ADDITIONAL_INFO: "application_summary_page",
            },
            PRIVATE_PERSON: {
                PERSON_DETAILS: "application_additional_information_page",
                ADDITIONAL_INFO: "application_summary_page",
            },
        }
        url_name = url_names[self.application_type][self.current_step]
        return reverse(
            f"core:{url_name}", kwargs={"uuid": self.application.uuid}
        )

    def get_next_step_redirect(self):
        """Returns redirect for application's next step"""
        return redirect(self.get_next_step_url())

    def get_context(self):
        """Returns application's step context"""
        previous_step_url, previous_step_title = self.get_previous_step_url()
        return {
            "webinar": self.webinar,
            "application": self.application,
            "previous_step_url": previous_step_url,
            "previous_step_title": previous_step_title,
            "step_number": self.get_step_number(),
            "step_title": self.get_step_title(),
            "step_description": self.get_step_description(),
            "application_timeline": self.get_timeline(),
        }

    def redirect_on_application_error(self):
        """Raise redirect exception if application can't be filled"""
        webinar: Webinar = self.application.webinar

        # If webinar is not in `homepage_webinars` queryset
        homepage_webinar_ids = Webinar.manager.init_or_confirmed().values_list(
            "id", flat=True
        )
        webinar_id: int = webinar.id  # type: ignore
        if webinar_id not in homepage_webinar_ids:
            raise RedirectException(
                reverse(
                    "core:webinar_program_page",
                    kwargs={"slug": self.webinar.slug},
                )
            )

        # If submitter is not set, redirect to form step
        if self.current_step == SUMMARY and self.application.submitter is None:
            if self.application.application_type == PRIVATE_PERSON:
                url_name = "core:application_person_details_page"
            else:
                url_name = "core:application_submitter_page"
            raise RedirectException(
                reverse(
                    url_name,
                    kwargs={"uuid": self.application.uuid},
                )
            )

    @staticmethod
    def transform_post_data(request: HttpRequest):
        """Transform POST data from `form repeater` to `formset` data

        Example:
            Key `kt_participants_repeater[0][first_name]`
            will be transformed to `form-0-first_name`

        Args:
            request (HttpRequest): Http request object

        Returns:
            HttpRequest: Http request with modifed POST data
        """
        transformed_post_keys = {}
        post_keys_to_delete = []

        # TODO: Potentially insecure, add some key checking with RegExp
        for post_key, post_value in request.POST.items():
            if not post_key.startswith("kt_participants_repeater"):
                continue
            post_keys_to_delete.append(post_key)
            key_index = post_key.split("][")[0].split("[")[1]
            field_name = post_key.split("-")[-1].strip("]")
            new_post_key = f"form-{key_index}-{field_name}"
            transformed_post_keys[new_post_key] = post_value

        # Yes I know this is kinda hacky but it works
        request.POST._mutable = True  # pylint: disable=protected-access

        # Delete post keys
        for key_to_delete in post_keys_to_delete:
            del request.POST[key_to_delete]

        # Add new keys
        for key, item in transformed_post_keys.items():
            request.POST[key] = item

        # Yes I know this is kinda hacky but it works
        request.POST._mutable = False  # pylint: disable=protected-access

        return request

    @staticmethod
    def populate_private_person_data(
        application: WebinarApplication,
        private_person: WebinarApplicationPrivatePerson,
    ):
        """Populate application fields based on private person data

        Args:
            application (WebinarApplication): application
            private_person (WebinarApplicationPrivatePerson): person data
        """

        # Save submitter
        if application.submitter:
            submitter: WebinarApplicationSubmitter = application.submitter
            submitter.first_name = private_person.first_name
            submitter.last_name = private_person.last_name
            submitter.email = private_person.email
            submitter.phone = private_person.phone
            submitter.save()
        else:
            submitter = WebinarApplicationSubmitter(
                first_name=private_person.first_name,
                last_name=private_person.last_name,
                email=private_person.email,
                phone=private_person.phone,
            )
            application.submitter = submitter  # type: ignore
            submitter.save()

        # Save participant
        # Delete all participants and save new one
        WebinarParticipant.manager.filter(application=application).delete()
        WebinarParticipant(
            application=application,
            first_name=private_person.first_name,
            last_name=private_person.last_name,
            email=private_person.email,
            phone=private_person.phone,
        ).save()

        # Save invoice
        if application.invoice:
            invoice = application.invoice
            invoice.invoice_email = private_person.email
            invoice.save()
        else:
            invoice = WebinarApplicationInvoice(
                invoice_email=private_person.email
            )
            application.invoice = invoice  # type: ignore
            invoice.save()

        # Save submitter
        if application.submitter:
            submitter = application.submitter
            submitter.first_name = private_person.first_name
            submitter.last_name = private_person.last_name
            submitter.email = private_person.email
            submitter.phone = private_person.phone
            submitter.save()
        else:
            submitter = WebinarApplicationSubmitter(
                first_name=private_person.first_name,
                last_name=private_person.last_name,
                email=private_person.email,
                phone=private_person.phone,
            )
            application.submitter = submitter  # type: ignore
            submitter.save()

        application.save()

    @staticmethod
    def save_submitter_as_participant(
        application: WebinarApplication, submitter: WebinarApplicationSubmitter
    ):
        """Save submitter as participant if `is_participant` checkbox is checked

        Args:
            application (WebinarApplication): _description_
            submitter (WebinarApplicationSubmitter): _description_
        """

        # Is user selected `is_participant`
        # and there is not participant with submitter's email already
        # in participants then save submitter as participant
        is_submiter_in_participants = WebinarParticipant.manager.filter(
            Q(application=application) & Q(email=submitter.email)
        ).exists()
        if all(
            [
                submitter.is_participant is True,
                not is_submiter_in_participants,
            ]
        ):
            WebinarParticipant(
                application=application,
                first_name=submitter.first_name,
                last_name=submitter.last_name,
                email=submitter.email,
                phone=submitter.phone,
            ).save()
