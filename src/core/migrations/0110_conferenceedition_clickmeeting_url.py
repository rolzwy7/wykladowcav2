# Generated by Django 4.2.2 on 2024-05-24 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0109_alter_conferenceedition_clickmeeting_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='conferenceedition',
            name='clickmeeting_url',
            field=models.CharField(default='clickmeeting_url', max_length=200, verbose_name='ClickMeeting URL'),
            preserve_default=False,
        ),
    ]
