# Generated by Django 4.2.2 on 2023-10-06 16:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0045_rename_click_count_webinarmetadata_click_count_mailing"),
    ]

    operations = [
        migrations.AddField(
            model_name="webinarmetadata",
            name="click_count_facebook",
            field=models.PositiveIntegerField(
                default=0, verbose_name="Kliknięcia Facebook"
            ),
        ),
        migrations.AddField(
            model_name="webinarmetadata",
            name="site_enter_count",
            field=models.PositiveIntegerField(
                default=0, verbose_name="Wejść na stronę"
            ),
        ),
        migrations.AlterField(
            model_name="webinarmetadata",
            name="click_count_mailing",
            field=models.PositiveIntegerField(
                default=0, verbose_name="Kliknięcia Mailing"
            ),
        ),
    ]