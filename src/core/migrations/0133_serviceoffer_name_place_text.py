# Generated by Django 4.2.2 on 2024-08-24 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0132_remove_serviceoffer_place_text_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceoffer',
            name='name_place_text',
            field=models.TextField(default='[NAME_PLACE_TEXT]', verbose_name='NAME_PLACE_TEXT'),
        ),
    ]
