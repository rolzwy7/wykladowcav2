# Generated by Django 4.2.2 on 2023-07-12 13:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0007_webinarapplicationmetadata_terms_accepted"),
    ]

    operations = [
        migrations.AddField(
            model_name="discountcode",
            name="discount_value",
            field=models.SmallIntegerField(
                default=5,
                help_text="W zależności od typu. Albo `zł` albo `%`",
                verbose_name="Wartość promocji",
            ),
        ),
    ]