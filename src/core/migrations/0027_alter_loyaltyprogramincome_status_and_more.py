# Generated by Django 4.2.2 on 2023-08-04 11:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0026_blacklisteddomain_blacklistedemail_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="loyaltyprogramincome",
            name="status",
            field=models.CharField(
                choices=[
                    ("PROCESSING", "W trakcie przetwarzania"),
                    ("PAYABLE", "Do wypłaty"),
                    ("VIOLATING", "Niezgodne z regulaminem"),
                ],
                default="PROCESSING",
                max_length=32,
                verbose_name="Status należności",
            ),
        ),
        migrations.AlterField(
            model_name="mailingcampaign",
            name="status",
            field=models.CharField(
                choices=[
                    ("PAUSED", "Zatrzymano"),
                    ("SENDING", "Wysyłanie"),
                    ("DONE", "Zakończono"),
                ],
                default="PAUSED",
                max_length=32,
            ),
        ),
    ]