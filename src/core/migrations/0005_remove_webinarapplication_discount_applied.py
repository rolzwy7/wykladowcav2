# Generated by Django 4.2.2 on 2023-07-12 11:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_rename_ref_code_webinarapplication_refcode"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="webinarapplication",
            name="discount_applied",
        ),
    ]
