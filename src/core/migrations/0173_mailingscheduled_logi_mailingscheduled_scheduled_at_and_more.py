# Generated by Django 4.2.2 on 2024-12-28 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0172_mailingscheduled_resignation_list_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailingscheduled',
            name='logi',
            field=models.TextField(blank=True, help_text='Logi', verbose_name='Logi'),
        ),
        migrations.AddField(
            model_name='mailingscheduled',
            name='scheduled_at',
            field=models.DateTimeField(help_text='Kiedy automat stworzył kampanie?', null=True, verbose_name='Stworzony automatycznie'),
        ),
        migrations.AlterField(
            model_name='mailingscheduled',
            name='schedule_after',
            field=models.DateTimeField(help_text='Po jakiej dacie ma być stworzona kampania?', verbose_name='Zaplanuj po dacie'),
        ),
        migrations.AlterField(
            model_name='mailingscheduled',
            name='target_date',
            field=models.DateField(help_text='Kiedy ma się wysyłać kampania?', verbose_name='Mailing na dzień'),
        ),
    ]
