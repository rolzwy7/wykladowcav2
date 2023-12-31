# Generated by Django 4.2.2 on 2023-08-08 15:05

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0029_alter_webinar_status"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="mailingcampaign",
            managers=[
                ("manager", django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name="lecturer",
            name="biography_email",
            field=models.TextField(blank=True, verbose_name="Biografia (e-mail)"),
        ),
    ]
