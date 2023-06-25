from django.forms.widgets import Textarea


class TextareaFloatingInputWidget(Textarea):
    template_name = "core/widgets/textarea_floating_input.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
