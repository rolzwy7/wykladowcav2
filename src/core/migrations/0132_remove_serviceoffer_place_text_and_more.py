# Generated by Django 4.2.2 on 2024-08-24 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0131_serviceoffer_file_text_serviceoffer_place_text_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serviceoffer',
            name='place_text',
        ),
        migrations.AddField(
            model_name='serviceoffer',
            name='nip_place_text',
            field=models.TextField(default='[NIP_PLACE_TEXT]', verbose_name='NIP_PLACE_TEXT'),
        ),
    ]