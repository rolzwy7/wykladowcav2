# Generated by Django 4.2.2 on 2025-01-08 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0179_mailingcampaign_is_dobijanie'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecturer',
            name='notes',
            field=models.TextField(blank=True, help_text='Widoczne tylko tutaj w CMS', verbose_name='Notatki'),
        ),
    ]