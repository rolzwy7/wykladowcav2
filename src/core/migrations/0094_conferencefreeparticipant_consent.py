# Generated by Django 4.2.2 on 2024-01-12 15:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0093_conferenceedition_categories"),
    ]

    operations = [
        migrations.AddField(
            model_name="conferencefreeparticipant",
            name="consent",
            field=models.BooleanField(default=False, verbose_name="Zgody marketingowe"),
        ),
    ]