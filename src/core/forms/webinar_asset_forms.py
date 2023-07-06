from django.forms import FileField, Form


class WebinarAssetForm(Form):
    """Form for webinar asset"""

    file = FileField()
