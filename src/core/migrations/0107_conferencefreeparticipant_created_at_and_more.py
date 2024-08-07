# Generated by Django 4.2.2 on 2024-05-24 09:19

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0106_alter_conferenceedition_cycle_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='conferencefreeparticipant',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='conferencefreeparticipant',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='conferenceedition',
            name='webinar',
            field=models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to='core.webinar', verbose_name='Webinar'),
        ),
    ]
