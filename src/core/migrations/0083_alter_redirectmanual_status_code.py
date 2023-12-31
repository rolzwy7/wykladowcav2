# Generated by Django 4.2.2 on 2023-12-12 15:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0082_alter_redirectmanual_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="redirectmanual",
            name="status_code",
            field=models.CharField(
                choices=[
                    ("301", "(301) Moved Permanently"),
                    ("302", "(302) Found"),
                    ("307", "(307) Temporary Redirect"),
                    ("308", "(308) Permanent Redirect"),
                ],
                max_length=10,
                verbose_name="Status code",
            ),
        ),
    ]
