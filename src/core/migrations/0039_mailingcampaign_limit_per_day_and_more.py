# Generated by Django 4.2.2 on 2023-09-03 14:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0038_webinarcategory_about_html"),
    ]

    operations = [
        migrations.AddField(
            model_name="mailingcampaign",
            name="limit_per_day",
            field=models.PositiveIntegerField(
                default=0, verbose_name="Limit wysłanych na dzień (0 = brak limitu)"
            ),
        ),
        migrations.AddField(
            model_name="mailingcampaign",
            name="limit_sent_so_far",
            field=models.PositiveIntegerField(
                default=0, verbose_name="Wysłano do tej pory"
            ),
        ),
        migrations.AddField(
            model_name="mailingcampaign",
            name="limit_timestamp",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="Limit reset datetime"
            ),
        ),
    ]