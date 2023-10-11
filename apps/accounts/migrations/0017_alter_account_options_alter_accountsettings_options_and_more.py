# Generated by Django 4.2.3 on 2023-09-27 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0016_account_is_marked_for_deletion"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="account",
            options={"verbose_name": "Account", "verbose_name_plural": "Accounts"},
        ),
        migrations.AlterModelOptions(
            name="accountsettings",
            options={
                "verbose_name": "Account setting",
                "verbose_name_plural": "Account settings",
            },
        ),
        migrations.AddField(
            model_name="account",
            name="date_deleted",
            field=models.DateTimeField(
                blank=True,
                help_text="Server date and time when the user deleted their account",
                null=True,
                verbose_name="Date deleted",
            ),
        ),
    ]