from django.db.models import CASCADE, CharField, ForeignKey, Model


class WebinarParticipant(Model):
    class Meta:
        verbose_name = "Uczestnicy"
        verbose_name_plural = "Uczestnik"

    webinar = ForeignKey("Webinar", on_delete=CASCADE, verbose_name="Webinar")
    first_name = CharField("Imię", max_length=100, blank=True)
    last_name = CharField("Nazwisko", max_length=100, blank=True)
    email = CharField("E-mail", max_length=100, blank=True)
    phone = CharField("Numer telefonu", max_length=100, blank=True)
