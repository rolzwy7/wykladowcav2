from django.forms import CharField, Form, Textarea


class CrmLecturerAddOpinionsForm(Form):
    """Form for adding opinions for lecturer in CRM panel"""

    opinions = CharField(widget=Textarea(attrs={"label": "Opinie"}))
