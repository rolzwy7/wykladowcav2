# Generated by Django 4.2.2 on 2024-10-05 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0145_alter_mailingcampaign_sent_start_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailingcampaign',
            name='target_code',
            field=models.CharField(blank=True, max_length=32, verbose_name='target_code'),
        ),
    ]
