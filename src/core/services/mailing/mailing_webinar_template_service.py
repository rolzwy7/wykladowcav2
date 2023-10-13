from random import shuffle

from django.conf import settings
from django.urls import reverse
from django.utils.timezone import now
from markdown import markdown

from core.consts.exemptions_consts import PRICE_ADNOTATION
from core.models import Webinar

COMPANY_NAME = settings.COMPANY_NAME
COMPANY_NIP = settings.COMPANY_NIP
BASE_URL = settings.BASE_URL


class MailingWebinarTemplateService:
    """Mailing Webinar Template Service"""

    def __init__(self, webinar: Webinar):
        self.webinar = webinar

    def get_td_classes(self) -> str:
        """Get td-tag classes"""
        td_classes = [
            "border-collapse:collapse;",
            "padding-left:20px;",
            "padding-right:20px;",
            "font-size: 16px;",
        ]
        shuffle(td_classes)
        return "".join(td_classes)

    def get_cta_text(self) -> str:
        """Get CTA text"""
        return "Zapisz się teraz!"

    def get_cta_href(self) -> str:
        """Get CTA href"""
        webinar_pk: int = self.webinar.pk
        webpath = reverse(
            "core:webinar_redirect_to_program", kwargs={"pk": webinar_pk}
        )
        return f"{BASE_URL}{webpath}"

    def antispam_text(self, text: str) -> str:
        """Transform text so it's not spam-like"""  # TODO
        ...

    def get_read_more_href(self) -> str:
        """Get read more href URL"""
        webinar_pk: int = self.webinar.pk
        webpath = reverse(
            "core:webinar_redirect_to_program", kwargs={"pk": webinar_pk}
        )
        return f"{BASE_URL}{webpath}"

    def get_read_more_text(self) -> str:
        """Get read more href URL"""
        return f"Czytaj cały program webinaru na stronie {COMPANY_NAME}"

    def get_program(self) -> str:
        """Get program"""
        lines = self.webinar.program_markdown.split("\n")
        new_program = ""
        for idx in range(int(len(lines) / 1.5)):
            new_program += f"{lines[idx]}\n"
        return markdown(new_program)

    def get_title(self) -> str:
        """Get title"""  # TODO
        ...

    def get_description(self) -> str:
        """Get description"""  # TODO
        ...

    def get_privacy_policy_href(self) -> str:
        """Get privacy policy href"""
        webpath = reverse("core:privacy_policy")
        return f"{BASE_URL}{webpath}"

    def get_context(self):
        """Get webinar template context"""
        td_classes = self.get_td_classes()

        return {
            "program": self.get_program(),
            "background_color": "#f1f4fa",
            "max_width": "640px",
            "td_classes": td_classes,
            "PRICE_ADNOTATION": PRICE_ADNOTATION,
            "cta_text": self.get_cta_text(),
            "cta_href": self.get_cta_href(),
            "read_more_href": self.get_read_more_href(),
            "read_more_text": self.get_read_more_text(),
            "privacy_policy_href": self.get_privacy_policy_href(),
            "BASE_URL": BASE_URL,
            "CURRENT_YEAR": now().year,
            "COMPANY_NAME": COMPANY_NAME,
            "COMPANY_NIP": COMPANY_NIP,
        }
