# Generated by Django 4.2.2 on 2023-12-30 13:06

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0087_webinar_program_short_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="BlacklistAggressor",
        ),
        migrations.DeleteModel(
            name="BlacklistPleading",
        ),
    ]
