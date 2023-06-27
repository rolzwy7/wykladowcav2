from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from .email_template import EmailTemplate


class EmailMessage:
    def __init__(
        self, email_template: EmailTemplate, subject: str, email: str
    ) -> None:
        self.email_template = email_template
        self.subject = subject
        self.email_message = EmailMultiAlternatives(
            subject=self.subject,
            body=self.email_template.text,
            from_email=f"{settings.COMPANY_NAME} <{settings.EMAIL_OFFICE}>",
            to=[email],
            cc=[settings.EMAIL_OFFICE],
            alternatives=[(self.email_template.html, "text/html")],
            headers={"Organization": settings.COMPANY_NAME_FULL},
            reply_to=[settings.EMAIL_OFFICE],
        )

    def attach(
        self, attachment_name: str, attachment_data: bytes, mime_type: str
    ):
        """Attach attachment to email message

        Example:
        message.attach("design.png", img_data, "image/png")

        Args:
            attachment_name (str): attachment name
            attachment_data (_type_): attachment data
            mime_type (str): mime type
        """
        self.email_message.attach(attachment_name, attachment_data, mime_type)

    def send(self) -> None:
        """Send email"""
        self.email_message.send(fail_silently=False)
