# Generated by Django 4.2.2 on 2023-12-08 10:07

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0063_alter_webinarapplicationinvoice_invoice_additional_info"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="webinarcategory",
            name="is_homepage_category",
        ),
    ]