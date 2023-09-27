# Generated by Django 4.2.3 on 2023-09-27 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "accounts",
            "0017_alter_account_options_alter_accountsettings_options_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="account",
            name="date_deleted",
        ),
        migrations.AddField(
            model_name="account",
            name="date_marked_for_deletion",
            field=models.DateTimeField(
                blank=True,
                help_text="Server date and time when the user deleted their                                                    account",
                null=True,
                verbose_name="Date marked for deletion",
            ),
        ),
    ]
