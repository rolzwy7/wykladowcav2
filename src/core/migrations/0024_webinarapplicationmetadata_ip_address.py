# Generated by Django 4.2.2 on 2023-07-31 17:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0023_webinar_recording_allowed"),
    ]

    operations = [
        migrations.AddField(
            model_name="webinarapplicationmetadata",
            name="ip_address",
            field=models.CharField(blank=True, max_length=64),
        ),
    ]
