# Generated by Django 4.2.2 on 2025-05-11 10:05

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0197_salerecordingapplication_fakturownia_payment_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='CrmNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('hide', models.BooleanField(default=False)),
                ('show_after', models.DateTimeField(auto_now_add=True)),
                ('hide_after', models.DateTimeField(auto_now_add=True)),
                ('note_title', models.TextField(verbose_name='Tytuł (HTML)')),
                ('note_content_html', models.TextField(blank=True, verbose_name='Treść (HTML)')),
                ('color', models.CharField(choices=[('primary', 'primary'), ('secondary', 'secondary'), ('success', 'success'), ('danger', 'danger'), ('warning', 'warning'), ('info', 'info')], default='primary', max_length=32, verbose_name='Kolor')),
            ],
            managers=[
                ('manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
