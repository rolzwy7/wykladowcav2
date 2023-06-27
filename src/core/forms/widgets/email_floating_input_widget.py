from .text_floating_input_widget import TextFloatingInputWidget


class EmailFloatingInputWidget(TextFloatingInputWidget):
    input_type = "email"
    template_name = "core/widgets/email_floating_input.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        return context
