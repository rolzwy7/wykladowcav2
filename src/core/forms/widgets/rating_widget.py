from django.forms.widgets import RadioSelect


class RatingWidget(RadioSelect):
    input_type = "radio"
    template_name = "core/widgets/rating_radio.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        return context
