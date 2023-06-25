from django.db.models import CASCADE, CharField, ForeignKey, Model


class WebinarParticipant(Model):
    application = ForeignKey(
        "WebinarApplication", on_delete=CASCADE, verbose_name="Zgłoszenie"
    )
    first_name = CharField("Imię", max_length=100)
    last_name = CharField("Nazwisko", max_length=100)
    email = CharField("E-mail", max_length=100)
    phone = CharField("Numer telefonu", max_length=100, blank=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.email})"

    class Meta:
        verbose_name = "Uczestnicy"
        verbose_name_plural = "Uczestnik"
