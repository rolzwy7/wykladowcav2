from .text_floating_input_widget import TextFloatingInputWidget


class PasswordFloatingInputWidget(TextFloatingInputWidget):
    input_type = "password"
    template_name = "core/widgets/password_floating_input.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        return context
