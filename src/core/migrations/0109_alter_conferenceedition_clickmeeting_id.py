# Generated by Django 4.2.2 on 2024-05-24 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0108_remove_conferenceedition_youtube_live_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conferenceedition',
            name='clickmeeting_id',
            field=models.CharField(max_length=200, verbose_name='ClickMeeting ID'),
        ),
    ]