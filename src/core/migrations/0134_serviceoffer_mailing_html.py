# Generated by Django 4.2.2 on 2024-08-25 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0133_serviceoffer_name_place_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceoffer',
            name='mailing_html',
            field=models.TextField(default='[MAILING_HTML]', verbose_name='MAILING_HTML'),
        ),
    ]
