# Generated by Django 4.2.2 on 2024-09-29 10:47

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0139_mailingcampaign_pause_on_too_many_failures'),
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(help_text='Fragment w URL', max_length=100, unique=True, verbose_name='Slug ankiety')),
                ('title', models.CharField(max_length=250, verbose_name='Tytuł')),
                ('description', models.TextField(blank=True, verbose_name='Opis')),
                ('user_creation_enabled', models.BooleanField(default=False, verbose_name='Dodawanie przez użytkownka aktywowane')),
            ],
            options={
                'verbose_name': 'Ankieta',
                'verbose_name_plural': 'Ankiety',
            },
            managers=[
                ('manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='SurveyAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=250, verbose_name='Tytuł')),
                ('user_created', models.BooleanField(default=False, verbose_name='Dodana przez użytkownika')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.survey', verbose_name='Ankieta')),
            ],
            options={
                'verbose_name': 'Ankieta (odpowiedź)',
                'verbose_name_plural': 'Ankiety (odpowiedzi)',
            },
            managers=[
                ('manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='SurveyVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('voter_id', models.CharField(max_length=100, verbose_name='ID głosującego')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.surveyanswer', verbose_name='Odpowiedź')),
            ],
            options={
                'verbose_name': 'Ankieta (głos)',
                'verbose_name_plural': 'Ankiety (głosy)',
            },
            managers=[
                ('manager', django.db.models.manager.Manager()),
            ],
        ),
    ]