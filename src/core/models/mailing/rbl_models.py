"""RBL models"""

# flake8: noqa=E501

from typing import Union

from django.db import models


class ListRBLManager(models.Manager):
    """Manager dla modelu ListRBL."""

    pass


class ListRBL(models.Model):
    """
    Model reprezentujący listę RBL (Real-time Blackhole List).
    """

    manager = ListRBLManager()

    # Definicja typów list RBL
    LIST_TYPE_CHOICES = [
        ("ip", "Adres IP"),
        ("domain", "Domena"),
        ("ip_domain", "IP i Domena"),
    ]

    address = models.CharField(
        max_length=255, unique=True, help_text="Adres listy RBL (np. zen.spamhaus.org)."
    )
    list_type = models.CharField(
        max_length=10,
        choices=LIST_TYPE_CHOICES,
        default="ip",
        help_text="Typ elementów, które śledzi ta lista RBL.",
    )
    is_important_list = models.BooleanField(
        default=False,
        help_text="Ważna lista",
    )

    def __str__(self):
        return f"{self.address} ({self.get_list_type_display()})"

    class Meta:
        verbose_name = "Lista RBL"
        verbose_name_plural = "Listy RBL"


class MonitorRBLManager(models.Manager):
    """Manager dla modelu MonitorRBL."""

    def get_latest(
        self, monitored_item: str, rbl_list: ListRBL
    ) -> Union["MonitorRBL", None]:
        """
        Zwraca ostatni (najnowszy) wpis w tabeli MonitorRBL.
        """
        return (
            self.get_queryset()
            .filter(
                models.Q(rbl_list=rbl_list) & models.Q(monitored_item=monitored_item)
            )
            .order_by("-created_at")
            .first()
        )


class MonitorRBL(models.Model):
    """
    Model reprezentujący wynik sprawdzenia na liście RBL w danym momencie.
    """

    manager = MonitorRBLManager()

    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Znacznik czasu, kiedy wykonano sprawdzenie."
    )
    monitored_item = models.CharField(
        max_length=255, help_text="Monitorowany adres IP lub domena.", db_index=True
    )
    rbl_list = models.ForeignKey(
        ListRBL,
        on_delete=models.CASCADE,
        related_name="monitoring_results",
        help_text="Lista RBL, na której dokonano sprawdzenia.",
    )
    response = models.TextField(
        blank=True, null=True, help_text="Odpowiedź otrzymana z serwera RBL."
    )
    is_blacklisted = models.BooleanField(
        default=False,
        help_text="Wskazuje, czy element został znaleziony na czarnej liście.",
    )

    def __str__(self):
        status = "Na czarnej liście" if self.is_blacklisted else "Czysty"
        return f"{self.monitored_item} na {self.rbl_list.address} - {status} o {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        """Meta"""

        verbose_name = "Wynik monitorowania RBL"
        verbose_name_plural = "Wyniki monitorowania RBL"
        ordering = ["-created_at"]
