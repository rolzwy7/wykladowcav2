# Generated by Django 4.2.2 on 2024-07-22 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0119_lecturer_years_experience'),
    ]

    operations = [
        migrations.AddField(
            model_name='webinarrecordingtoken',
            name='starts_at',
            field=models.DateTimeField(blank=True, help_text='Puste pole oznacza, że token jest ważny od momentu stworzenia', null=True, verbose_name='Ważny od'),
        ),
        migrations.AlterField(
            model_name='smtpsender',
            name='incoming_server_port',
            field=models.CharField(choices=[('110', '110'), ('143', '143'), ('993', '993'), ('995', '995')], max_length=5, verbose_name='Serwer przychodzący Port'),
        ),
        migrations.AlterField(
            model_name='smtpsender',
            name='outgoing_server_port',
            field=models.CharField(choices=[('25', '25'), ('465', '465'), ('587', '587')], max_length=5, verbose_name='Serwer wychodzący Port'),
        ),
        migrations.AlterField(
            model_name='webinarrecordingtoken',
            name='expires_at',
            field=models.DateTimeField(blank=True, help_text='Puste pole oznacza, że token nie wygasa nigdy', null=True, verbose_name='Ważny do'),
        ),
    ]