# Generated by Django 4.2.2 on 2024-10-14 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0148_serviceofferapplication_uncertain'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceofferapplication',
            name='accepted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='serviceofferapplication',
            name='sent_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
