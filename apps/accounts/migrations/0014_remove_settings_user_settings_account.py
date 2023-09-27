# Generated by Django 4.2.3 on 2023-09-27 11:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0013_rename_site_updates_settings_site_update_emails"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="settings",
            name="user",
        ),
        migrations.AddField(
            model_name="settings",
            name="account",
            field=models.OneToOneField(
                default=1,
                help_text="Account settings",
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Account",
            ),
            preserve_default=False,
        ),
    ]
