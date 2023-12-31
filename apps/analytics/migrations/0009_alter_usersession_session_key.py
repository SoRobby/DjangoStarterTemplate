# Generated by Django 4.2.5 on 2023-10-24 22:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("analytics", "0008_alter_objectviewed_content_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usersession",
            name="session_key",
            field=models.CharField(
                default=django.utils.timezone.now,
                help_text="Session key",
                max_length=40,
            ),
            preserve_default=False,
        ),
    ]
