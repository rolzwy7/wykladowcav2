# Generated by Django 4.2.2 on 2023-10-20 11:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0048_webinar_grouping_token"),
    ]

    operations = [
        migrations.AddField(
            model_name="webinar",
            name="is_fake",
            field=models.BooleanField(default=False, verbose_name="Fake'owy termin"),
        ),
        migrations.AlterField(
            model_name="webinar",
            name="slug",
            field=models.SlugField(
                blank=True,
                help_text="Unikalny skrót pojawiający się w adresie URL (Ważne dla SEO)",
                max_length=230,
                unique=True,
                verbose_name="Skrót URL",
            ),
        ),
    ]