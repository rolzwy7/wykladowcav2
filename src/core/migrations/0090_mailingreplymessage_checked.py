# Generated by Django 4.2.2 on 2023-12-30 14:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0089_mailingreplymessage_blacklistedemail_message_content_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="mailingreplymessage",
            name="checked",
            field=models.BooleanField(default=False),
        ),
    ]
