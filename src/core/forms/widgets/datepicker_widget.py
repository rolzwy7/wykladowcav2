from django.forms.widgets import DateTimeInput


class DatepickerWidget(DateTimeInput):
    input_type = "text"
    template_name = "core/widgets/datepicker.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        return context
