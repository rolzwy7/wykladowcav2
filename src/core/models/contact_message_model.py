from django.db.models import (
    CharField,
    DateTimeField,
    EmailField,
    Manager,
    Model,
    QuerySet,
    TextField,
)
from django.utils.timezone import now, timedelta


class ContactMessageManager(Manager):
    """Contact Message Manager"""

    def crm_visible(self) -> QuerySet["ContactMessage"]:
        """Contact messages visible in CRM"""
        return self.get_queryset().filter(
            created_at__gte=now() - timedelta(days=30)
        )

    def newest_count(self) -> int:
        """Get count of newest question to be displayed in leftbar"""
        return (
            self.get_queryset()
            .filter(created_at__gte=now() - timedelta(hours=30))
            .count()
        )


class ContactMessage(Model):
    """Represents webinar's asset"""

    manager = ContactMessageManager()

    created_at = DateTimeField(auto_now_add=True)

    first_name = CharField("Imię", max_length=64)

    last_name = CharField("Nazwisko", max_length=64)

    email = EmailField("Adres e-mail")

    phone_number = CharField("Numer telefonu", max_length=64, blank=True)

    message = TextField("Wiadomość", max_length=1000)

    related_to = CharField("Nawiązuje do", max_length=264, blank=True)

    class Meta:
        verbose_name = "Wiadomość kontaktowa"
        verbose_name_plural = "Wiadomość kontaktowa"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
