# Generated by Django 4.2.2 on 2023-09-03 14:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0039_mailingcampaign_limit_per_day_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="mailingcampaign",
            name="stat_procesed",
            field=models.PositiveIntegerField(
                default=0, verbose_name="Przetworzono (stat)"
            ),
        ),
        migrations.AddField(
            model_name="mailingcampaign",
            name="stat_sent",
            field=models.PositiveIntegerField(default=0, verbose_name="Wysłano (stat)"),
        ),
    ]