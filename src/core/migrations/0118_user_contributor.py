# Generated by Django 4.2.2 on 2024-06-24 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0117_webinarapplicationtracking'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='contributor',
            field=models.BooleanField(default=False, verbose_name='Udzielający się'),
        ),
    ]