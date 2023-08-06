from django.forms import CharField, FileField, Form

from core.forms.widgets import CheckboxWidget


class MailingAddEmailsForm(Form):
    """Form for adding emails to mailing campaign"""

    file = FileField()


class MailingDeleteEmailsAreYouSureForm(Form):
    """Form for confirming deleting all emails from mailing campaign"""

    i_am_sure = CharField(
        widget=CheckboxWidget(attrs={"label": "Chcę wykonać tę operację"})
    )
