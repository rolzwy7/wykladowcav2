# Generated by Django 4.2.2 on 2023-12-08 15:49

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0065_alter_webinarcategory_parent"),
    ]

    operations = [
        migrations.CreateModel(
            name="CategoryTrustedUs",
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
                (
                    "visible",
                    models.BooleanField(
                        default=True, verbose_name="Widoczna na stronie"
                    ),
                ),
                (
                    "company_name",
                    models.CharField(max_length=100, verbose_name="Nazwa firmy"),
                ),
                (
                    "company_logo",
                    models.ImageField(
                        help_text="Obrazek powinien być dobrej jakości o wymiarach najlepiej kwadratowych",
                        upload_to="uploads/trusted_us_logos",
                        verbose_name="Logo firmy",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="core.webinarcategory",
                    ),
                ),
            ],
            options={
                "verbose_name": "Kategoria (zaufali name)",
                "verbose_name_plural": "Kategorie (zaufali name)",
            },
            managers=[
                ("manager", django.db.models.manager.Manager()),
            ],
        ),
    ]