# Generated by Django 4.2.2 on 2023-10-13 17:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0046_webinarmetadata_click_count_facebook_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="webinar",
            name="discount_netto",
            field=models.PositiveSmallIntegerField(
                blank=True, default=0, null=True, verbose_name="Cena NETTO (Promocyjna)"
            ),
        ),
    ]
