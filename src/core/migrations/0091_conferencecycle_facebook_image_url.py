# Generated by Django 4.2.2 on 2024-01-04 13:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0090_mailingreplymessage_checked"),
    ]

    operations = [
        migrations.AddField(
            model_name="conferencecycle",
            name="facebook_image_url",
            field=models.CharField(
                blank=True, max_length=250, verbose_name="Facebook image"
            ),
        ),
    ]
