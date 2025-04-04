from django.forms import CharField, EmailField, FileField, Form

from core.forms.widgets import CheckboxWidget, EmailFloatingInputWidget


class MailingAddEmailsForm(Form):
    """Form for adding emails to mailing campaign"""

    file = FileField()


class MailingSendTestEmailForm(Form):
    """Form for sending test email for mailing campaign"""

    email = EmailField(
        widget=EmailFloatingInputWidget(
            attrs={"label": "Adres E-mail", "autofocus": "autofocus"}
        )
    )


class MailingAreYouSureForm(Form):
    """Form for confirming operations for mailing campaign"""

    i_am_sure = CharField(
        widget=CheckboxWidget(attrs={"label": "Chcę wykonać tę operację"})
    )
