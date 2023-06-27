from django.forms.widgets import TextInput


class TextFloatingInputWidget(TextInput):
    input_type = "text"
    template_name = "core/widgets/text_floating_input.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        return context
