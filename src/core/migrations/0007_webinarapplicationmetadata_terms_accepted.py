# Generated by Django 4.2.2 on 2023-07-12 12:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0006_discountcode_discountapplicationapplied"),
    ]

    operations = [
        migrations.AddField(
            model_name="webinarapplicationmetadata",
            name="terms_accepted",
            field=models.BooleanField(
                default=False, verbose_name="Zaakceptowano regulamin"
            ),
        ),
    ]
