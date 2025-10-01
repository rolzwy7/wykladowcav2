"""ClosedWebinarContactMessage Model"""

# flake8: noqa=E501

from django.db import models


class ClosedWebinarContactMessage(models.Model):
    """ClosedWebinarContactMessage"""

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data utworzenia")

    full_name = models.CharField(max_length=100, verbose_name="Imię i nazwisko")
    company = models.CharField(max_length=100, blank=True, verbose_name="Firma")
    number_of_participants = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Potencjalna liczba osób do przeszkolenia",
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    email = models.EmailField(verbose_name="Email")
    message = models.TextField(max_length=1000, verbose_name="Treść wiadomości")

    tracking_info = models.CharField(max_length=100, blank=True)

    spy_object = models.ForeignKey(
        "SpyObject",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Spy Object",
    )

    def __str__(self):
        return f"{self.full_name} - {self.email}"

    class Meta:
        verbose_name = "Wiadomość kontaktowa (szkolenie zamknięte)"
        verbose_name_plural = "Wiadomości kontaktowe (szkolenie zamknięte)"
