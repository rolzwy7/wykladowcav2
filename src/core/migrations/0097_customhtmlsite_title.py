# Generated by Django 4.2.2 on 2024-01-15 09:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0096_customhtmlsite"),
    ]

    operations = [
        migrations.AddField(
            model_name="customhtmlsite",
            name="title",
            field=models.CharField(blank=True, max_length=250, verbose_name="Tytuł"),
        ),
    ]