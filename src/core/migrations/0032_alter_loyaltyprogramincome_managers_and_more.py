# Generated by Django 4.2.2 on 2023-08-15 10:50

from django.db import migrations, models
import django.db.models.manager
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0031_webinarcategory_icon_html_and_more"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="loyaltyprogramincome",
            managers=[
                ("manager", django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name="loyaltyprogrampayout",
            managers=[
                ("manager", django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name="mailingcampaign",
            name="send_after",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="Wysyłaj po"
            ),
        ),
        migrations.AlterField(
            model_name="loyaltyprogrampayout",
            name="invoice_attachment",
            field=models.FileField(upload_to="uploads/loyalty_payouts"),
        ),
    ]