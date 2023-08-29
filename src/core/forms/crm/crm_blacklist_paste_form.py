from django.forms import CharField, Form, Textarea


class CrmBlacklistPasteForm(Form):
    """Form for adding blacklists in CRM panel"""

    blacklist_lines = CharField(widget=Textarea())
