# Generated by Django 4.2.2 on 2024-10-22 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0152_survey_add_placeholder_survey_search_placeholder'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveyanswer',
            name='lecturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.lecturer', verbose_name='Wykładowca'),
        ),
    ]