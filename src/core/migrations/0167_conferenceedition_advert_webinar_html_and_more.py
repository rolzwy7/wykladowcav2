# Generated by Django 4.2.2 on 2024-12-04 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0166_conferenceedition_advert_facebook_html_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='conferenceedition',
            name='advert_webinar_html',
            field=models.TextField(blank=True, verbose_name='Advert FB HTML'),
        ),
        migrations.AddField(
            model_name='conferenceedition',
            name='advert_webinar_url',
            field=models.CharField(blank=True, max_length=200, verbose_name='Advert FB URL'),
        ),
    ]