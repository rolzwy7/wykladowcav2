# Generated by Django 4.2.2 on 2023-07-27 14:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):
    dependencies = [
        (
            "core",
            "0020_rename_participants_count_webinarmoveregister_applications_count",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="LoyaltyProgram",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "ref_number",
                    models.CharField(max_length=32, primary_key=True, serialize=False),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Użytkownik",
                    ),
                ),
            ],
            options={
                "verbose_name": "Program partnerski (Użytkownik)",
                "verbose_name_plural": "Program partnerski (Użytkownicy)",
            },
            managers=[
                ("manager", django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name="webinarmoveregister",
            name="applications_count",
            field=models.PositiveSmallIntegerField(
                help_text="Ilość zgłoszeń w momencie przenoszenia",
                verbose_name="Ilość zgłoszeń",
            ),
        ),
        migrations.CreateModel(
            name="LoyaltyProgramPayout",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("WAITING_FOR_CONFIRMATION", "Czeka na potwierdzenie"),
                            ("PAYED", "Zapłacono"),
                            ("REFUSED", "Odmówiono zapłaty"),
                        ],
                        default="WAITING_FOR_CONFIRMATION",
                        max_length=32,
                        verbose_name="Status należności",
                    ),
                ),
                (
                    "note_employee",
                    models.TextField(
                        blank=True, verbose_name="Uwagi do wypłaty (pracownik)"
                    ),
                ),
                (
                    "payout_brutto",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Wartość Brutto"
                    ),
                ),
                ("invoice_attachment", models.FileField(upload_to="")),
                (
                    "loyalty_program",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.loyaltyprogram",
                        verbose_name="Kod referencyjny",
                    ),
                ),
            ],
            options={
                "verbose_name": "Program partnerski (Wypłata)",
                "verbose_name_plural": "Program partnerski (Wypłaty)",
            },
        ),
        migrations.CreateModel(
            name="LoyaltyProgramIncome",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PROCESSING", "PROCESSING"),
                            ("PAYABLE", "PAYABLE"),
                            ("VIOLATING", "VIOLATING"),
                        ],
                        default="PROCESSING",
                        max_length=32,
                        verbose_name="Status należności",
                    ),
                ),
                (
                    "note_employee",
                    models.TextField(
                        blank=True, verbose_name="Uwagi do należności (pracownik)"
                    ),
                ),
                (
                    "amount_brutto",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Wartość Brutto"
                    ),
                ),
                (
                    "application",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.webinarapplication",
                        verbose_name="Zgłoszenie",
                    ),
                ),
                (
                    "loyalty_program",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.loyaltyprogram",
                        verbose_name="Kod referencyjny",
                    ),
                ),
            ],
            options={
                "verbose_name": "Program partnerski (Należność)",
                "verbose_name_plural": "Program partnerski (Należności)",
            },
        ),
    ]
