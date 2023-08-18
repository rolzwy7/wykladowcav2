from django.db.models import CharField, Model, TextField
from html2text import HTML2Text


class MailingTemplate(Model):
    """Represents mailing template"""

    name = CharField("Nazwa szablonu", max_length=100)
    html = TextField("HTML")
    text = TextField("TEXT", blank=True)

    class Meta:
        verbose_name = "Szablon mailingowy"
        verbose_name_plural = "Szablony mailingowe"

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs) -> None:
        # Create text version of email template
        if not self.text:
            self.create_text_version_from_html()
        return super().save(*args, **kwargs)

    def create_text_version_from_html(self):
        """Create text version from HTML"""
        html2text = HTML2Text()
        self.text = html2text.handle(self.html)
