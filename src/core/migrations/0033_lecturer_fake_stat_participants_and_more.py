# Generated by Django 4.2.2 on 2023-08-29 10:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0032_alter_loyaltyprogramincome_managers_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="lecturer",
            name="fake_stat_participants",
            field=models.PositiveIntegerField(
                default=0, verbose_name="Przeszkolonych (baza)"
            ),
        ),
        migrations.AddField(
            model_name="lecturer",
            name="fake_stat_webinars",
            field=models.PositiveIntegerField(
                default=0, verbose_name="Przeprowadzonych szkoleń (baza)"
            ),
        ),
    ]
